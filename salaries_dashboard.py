import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. إعداد الصفحة
st.set_page_config(layout="wide", page_title="تحليل مرتبات شركة قها للمنتجات الغذائية")

# ---------------------------------------------------------
# تنسيق CSS (توسيط الكروت + الاتجاهات)
# ---------------------------------------------------------
st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; }
    div.block-container { direction: rtl; text-align: right; }
    div[data-testid="stSidebarUserContent"] { text-align: right; direction: rtl; }
    
    /* تنسيق الكروت لتكون في المنتصف */
    div[data-testid="metric-container"] {
        direction: ltr; 
        text-align: center;
        background-color: #f8f9fa;
        border: 1px solid #ddd;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    div[data-testid="stMetricLabel"] { justify-content: center; width: 100%; text-align: center; font-weight: bold; color: #333;}
    div[data-testid="stMetricValue"] { justify-content: center; text-align: center; width: 100%; color: #007bff; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. دالة تحميل البيانات
# ---------------------------------------------------------
@st.cache_data
def load_data():
    # تحديد مسار الملف بجوار الكود
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'salaries2.xlsx')
    
    if not os.path.exists(file_path):
        st.error(f"❌ File not found at: {file_path}")
        return None
    
    # قراءة الملف
    df = pd.read_excel(file_path, header=2)
    
    # تنظيف الأعمدة
    df.columns = df.columns.astype(str).str.strip()
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # تنظيف الصفوف
    if 'الاسم' in df.columns and 'الادارة' in df.columns:
        df.dropna(subset=['الاسم', 'الادارة'], inplace=True)
        df['الادارة'] = df['الادارة'].astype(str)
        
        # حذف "اسم العامل" و "الاجماليات"
        df = df[~df['الادارة'].str.contains('سم العامل', na=False)]
        df = df[~df['الادارة'].str.contains('اجمالى', na=False)]
    
    # تحويل الأرقام
    numeric_cols = ['اجمالى المستحق', 'اجمالى الأستقطاعات', 'اجمالى حافز الانتاج', 'صافى الراتب']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # تصنيف الراتب
    if 'صافى الراتب' in df.columns:
        df['salary_category'] = df['صافى الراتب'].apply(
            lambda x: "High" if x >= 5000 else ("Medium" if x >= 3000 else "Low")
        )
        
    return df  # <--- (تم التأكد: الكلمة في مكانها الصحيح)

# استدعاء الدالة
df = load_data()

# ---------------------------------------------------------
# 3. عرض اللوجو والقائمة الجانبية
# ---------------------------------------------------------

# مسار اللوجو
current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, 'logo.png') # تأكدي أن الصورة اسمها logo.png

# عرض اللوجو في القائمة الجانبية
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=150) # يمكنك تغيير الرقم لتكبير/تصغير الصورة
else:
    st.sidebar.markdown("## 🏢 Qaha Salaries Analysis") # لو الصورة مش موجودة يكتب نص

# ---------------------------------------------------------
# 4. بناء الداش بورد
# ---------------------------------------------------------
if df is not None:
    if 'الادارة' not in df.columns:
        st.error("Error: Column 'الادارة' not found!")
    else:
        # الفلتر (Dropdown)
        st.sidebar.header("Filter Settings")
        dept_list = sorted(df['الادارة'].unique())
        dept_options = ['All Departments'] + dept_list
        
        selected_dept = st.sidebar.selectbox(
            "Select Department:",
            options=dept_options
        )
        
        if selected_dept == 'All Departments':
            df_filtered = df.copy()
        else:
            df_filtered = df[df['الادارة'] == selected_dept]

        # العنوان الرئيسي
        st.title("📊 HR & Salaries Dashboard")
        st.markdown("---")

        # الكروت (KPIs)
        col1, col2, col3, col4 = st.columns(4)
        
        emp_count = df_filtered['الاسم'].nunique()
        dept_count = df_filtered['الادارة'].nunique()
        
        total_sal = df_filtered['اجمالى المستحق'].sum()
        total_deduct = df_filtered['اجمالى الأستقطاعات'].sum()
        total_incentive = df_filtered['اجمالى حافز الانتاج'].sum()
        
        pct_deduct = (total_deduct / total_sal * 100) if total_sal > 0 else 0
        pct_incentive = (total_incentive / total_sal * 100) if total_sal > 0 else 0

        col1.metric("Total Employees", emp_count)
        col2.metric("Total Departments", dept_count)
        col3.metric("Deduction Ratio", f"{pct_deduct:.2f}%")
        col4.metric("Incentive Ratio", f"{pct_incentive:.2f}%")

        st.markdown("---")

        # الرسومات البيانية
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Employees per Department")
            dept_data = df_filtered['الادارة'].value_counts().reset_index()
            dept_data.columns = ['Department', 'Count']
            fig1 = px.bar(dept_data.head(10), x='Department', y='Count', text='Count', color='Department')
            st.plotly_chart(fig1, use_container_width=True)
            
        with c2:
            st.subheader("Salary Categories")
            pie_data = df_filtered['salary_category'].value_counts().reset_index()
            pie_data.columns = ['Category', 'Count']
            fig2 = px.pie(pie_data, values='Count', names='Category', hole=0.4,
                          color_discrete_map={'High':'#2ecc71', 'Medium':'#f1c40f', 'Low':'#e74c3c'})
            st.plotly_chart(fig2, use_container_width=True)

        c3, c4 = st.columns(2)
        with c3:
            st.subheader("Top 5 Costly Departments")
            cost_data = df_filtered.groupby('الادارة')['صافى الراتب'].sum().nlargest(5).reset_index()
            fig3 = px.bar(cost_data, x='الادارة', y='صافى الراتب', text_auto='.2s', color='الادارة')
            st.plotly_chart(fig3, use_container_width=True)

        with c4:
            st.subheader("Average Salary")
            avg_data = df_filtered.groupby('الادارة')['صافى الراتب'].mean().sort_values(ascending=False).head(10).reset_index()
            fig4 = px.bar(avg_data, x='الادارة', y='صافى الراتب', color='صافى الراتب')
            st.plotly_chart(fig4, use_container_width=True)

        c5, c6 = st.columns(2)
        with c5:
            st.subheader("Stacked Analysis")
            stack_data = df_filtered.groupby(['الادارة', 'salary_category']).size().reset_index(name='count')
            top_depts = df_filtered['الادارة'].value_counts().head(10).index
            stack_data = stack_data[stack_data['الادارة'].isin(top_depts)]
            fig5 = px.bar(stack_data, x='الادارة', y='count', color='salary_category', barmode='stack')
            st.plotly_chart(fig5, use_container_width=True)
            
        with c6:
            st.subheader("Outliers Detection (Boxplot)")
            q1 = df_filtered['صافى الراتب'].quantile(0.25)
            q3 = df_filtered['صافى الراتب'].quantile(0.75)
            iqr = q3 - q1
            clean_df = df_filtered[(df_filtered['صافى الراتب'] >= (q1 - 1.5*iqr)) & (df_filtered['صافى الراتب'] <= (q3 + 1.5*iqr))]
            
            fig6 = px.box(clean_df, y='صافى الراتب', x='الادارة')
            if len(dept_options) > 10: fig6.update_xaxes(range=[-0.5, 9.5])
            st.plotly_chart(fig6, use_container_width=True)

else:
    st.info("Loading Data...")