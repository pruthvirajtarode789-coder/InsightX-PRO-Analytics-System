# app/streamlit_app.py
import streamlit as st, pandas as pd, os, requests
import plotly.express as px
import streamlit.components.v1 as components
import plotly.graph_objects as go
st.set_page_config(layout='wide', page_title='InsightX PRO')

API_URL = st.secrets.get('API_URL', 'http://127.0.0.1:8000')

# ===== Custom styling =====
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    .app-header{
        background: linear-gradient(90deg,#0b3d91 0%, #1b6fd8 100%);
        padding: 18px 24px;
        border-radius: 10px;
        color: white;
        margin-bottom: 18px;
        box-shadow: 0 8px 30px rgba(11,61,145,0.12);
    }
    .kpi-card{
        background: linear-gradient(180deg, #ffffffcc, #f6f8ffcc);
        border-radius: 12px;
        padding: 14px;
        box-shadow: 0 6px 18px rgba(11,61,145,0.08);
        text-align: left;
    }
    .kpi-value{font-size:22px;font-weight:700;color:#0b3d91}
    .kpi-label{font-size:13px;color:#556080}
    .small-muted{color:#778099;font-size:12px}
    .section-title{font-weight:700;color:#0b3d91;margin-bottom:8px}

    /* Dark theme overrides */
    .theme-dark .app-header{background:linear-gradient(90deg,#0b284f 0%, #0e3b7a 100%);}
    .theme-dark .kpi-card{background:linear-gradient(180deg,#0b1b2bcc,#071428cc);color:#e6eefc}
    .theme-dark .kpi-value{color:#9ecbff}
    .theme-dark .kpi-label{color:#9bb0d1}
    .theme-dark .section-title{color:#9ecbff}

    /* Segmentation badges */
    .seg-badge{display:inline-block;padding:6px 10px;border-radius:999px;margin:4px 6px;font-weight:600;color:#fff}
    .seg-0{background:#ff6b6b}
    .seg-1{background:#ffa94d}
    .seg-2{background:#4dabf7}
    .seg-3{background:#63e6be}
    .seg-4{background:#b197fc}
    .footer{color:#9aa7c7;font-size:12px;margin-top:18px;padding-top:8px;border-top:1px solid rgba(0,0,0,0.04)}
    </style>
    """,
    unsafe_allow_html=True,
)

# Theme / session
if 'theme' not in st.session_state:
        st.session_state.theme = 'light'

# Sidebar: small logo and theme toggle
st.sidebar.markdown('<div style="text-align:center;margin-bottom:8px"><strong style="font-size:18px;color:#0b3d91">InsightX PRO</strong><div class="small-muted">Analytics & Forecasting</div></div>', unsafe_allow_html=True)
theme_choice = st.sidebar.radio('Theme', ['Light', 'Dark'], index=0 if st.session_state.theme == 'light' else 1)
st.session_state.theme = 'light' if theme_choice == 'Light' else 'dark'

# JS to add theme class to body for CSS scoping
components.html(f"""
<script>
    document.body.classList.remove('theme-light','theme-dark');
    document.body.classList.add('theme-{st.session_state.theme}');
</script>
""", height=0)

# Header
st.markdown(
        f"""
        <div class="app-header">
            <div style="display:flex;align-items:center;justify-content:space-between;">
                <div style="display:flex;align-items:center;gap:14px;">
                    <div style="width:44px;height:44px;background:rgba(255,255,255,0.12);border-radius:8px;display:flex;align-items:center;justify-content:center">
                        <!-- simple SVG logo -->
                        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="2" y="3" width="20" height="18" rx="3" fill="white" fill-opacity="0.12"/><path d="M6 8h12M6 12h12M6 16h8" stroke="white" stroke-opacity="0.9" stroke-width="1.2" stroke-linecap="round"/></svg>
                    </div>
                    <div style="font-size:20px;font-weight:800;">InsightX PRO</div>
                    <div style="font-size:13px;opacity:0.95">Analytics & Forecasting — interactive demo</div>
                </div>
                <div style="display:flex;align-items:center;gap:12px">
                    <div style="font-size:13px;opacity:0.9">Theme: {st.session_state.theme.title()}</div>
                    <div style="font-size:12px;color:#ffffffaa;background:rgba(255,255,255,0.06);padding:6px 10px;border-radius:8px">v1.0</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
)

data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sales_sample.csv')
df = pd.read_csv(data_path, parse_dates=['date'])

st.sidebar.title('Controls')
view = st.sidebar.selectbox('View', ['Overview','Forecast','Segmentation','Anomalies','About'])

if view == 'Overview':
    st.markdown('<div class="section-title">Overview</div>', unsafe_allow_html=True)
    total_revenue = df['revenue'].sum()
    total_orders = df['quantity'].sum()
    active_customers = df['customer_id'].nunique()
    c1, c2, c3 = st.columns(3)
    # Animated KPI cards using a small JS counter inside iframe
    def kpi_card(label, value, key):
        html = f"""
        <div class="kpi-card">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value" id="val-{key}">0</div>
        </div>
        <script>
        const el = document.getElementById('val-{key}');
        const target = {int(value)};
        let cur = 0;
        const step = Math.max(1, Math.round(target/40));
        const t = setInterval(()=>{{
          cur = Math.min(target, cur + step);
          el.innerText = new Intl.NumberFormat().format(cur);
          if(cur>=target) clearInterval(t);
        }}, 20);
        </script>
        """
        return html

    with c1:
        components.html(kpi_card('Total Revenue', total_revenue, 'rev'), height=80)
    with c2:
        components.html(kpi_card('Total Orders', int(total_orders), 'orders'), height=80)
    with c3:
        components.html(kpi_card('Active Customers', int(active_customers), 'custs'), height=80)
    st.markdown('---')
    st.markdown('<div class="section-title">Revenue by product</div>', unsafe_allow_html=True)
    prod_df = df.groupby('product_id')['revenue'].sum().reset_index().sort_values('revenue', ascending=False)
    fig = px.bar(prod_df, x='product_id', y='revenue', text='revenue', title='Revenue by Product', labels={'product_id':'Product','revenue':'Revenue'})
    fig.update_layout(margin=dict(l=0,r=0,t=30,b=0), template='seaborn')
    st.plotly_chart(fig, use_container_width=True)

elif view == 'Forecast':
    st.subheader('Forecasting (calls backend)')
    prod = st.selectbox('Product (optional)', options=[None]+sorted(df['product_id'].unique().tolist()))
    days = st.slider('Forecast days', 7, 90, 30)
    if st.button('Run Forecast'):
        payload = {'product_id': prod, 'days': int(days)}
        try:
            r = requests.post(f'{API_URL}/forecast', json=payload, timeout=20)
            data = r.json()
            fc = pd.DataFrame(data['forecast'])
            fc['date'] = pd.to_datetime(fc['date'])
            st.line_chart(fc.set_index('date')['forecast'])
        except Exception as e:
            st.error('API call failed: '+str(e))

elif view == 'Segmentation':
    st.subheader('Customer Segmentation (call API)')
    n = st.slider('Number of clusters', 2, 8, 4)
    if st.button('Run Segmentation'):
        try:
            r = requests.post(f'{API_URL}/segment', json={'n_clusters': int(n)}, timeout=20)
            data = r.json()
            # counts -> bar chart
            counts = data.get('counts', {})
            if counts:
                counts_df = pd.DataFrame({'segment': list(counts.keys()), 'count': list(counts.values())})
                counts_df['segment'] = counts_df['segment'].astype(int)
                st.markdown('**Cluster counts**')
                # show badges
                badge_html = ""
                for seg, cnt in counts.items():
                    cls = f'seg-{int(seg) % 5}'
                    badge_html += f"<span class='seg-badge {cls}'>Cluster {seg}: {cnt}</span>"
                st.markdown(badge_html, unsafe_allow_html=True)
                st.plotly_chart(px.pie(counts_df, names='segment', values='count', title='Segments distribution'), use_container_width=True)
            # sample -> table + scatter
            sample = data.get('sample', [])
            if sample:
                samp_df = pd.DataFrame(sample)
                st.markdown('**Sample customers (first 10)**')
                st.dataframe(samp_df)
                # scatter plot of customers by orders vs avg value colored by segment if available
                if {'total_orders', 'avg_order_value', 'segment'}.issubset(samp_df.columns):
                    st.markdown('**Segment visualization**')
                    try:
                        fig = px.scatter(samp_df, x='total_orders', y='avg_order_value', color=samp_df['segment'].astype(str),
                                         hover_data=['customer_id','tenure_days'], title='Customers: Orders vs Avg Order Value',
                                         labels={'total_orders':'Total Orders','avg_order_value':'Avg Order Value'})
                        fig.update_traces(marker=dict(line=dict(width=0.5,color='#ffffffcc')))
                        col1, col2 = st.columns([2,3])
                        with col1:
                            st.plotly_chart(fig, use_container_width=True)
                        with col2:
                            st.markdown('**Segment Details**')
                            st.write(samp_df[['customer_id','total_orders','avg_order_value','tenure_days','segment']].reset_index(drop=True))
                    except Exception:
                        pass
        except Exception as e:
            st.error('API call failed: '+str(e))

elif view == 'Anomalies':
    st.subheader('Anomaly Detection (call API)')
    thr = st.slider('Std threshold', 0.5, 4.0, 2.0)
    if st.button('Detect Anomalies'):
        try:
            r = requests.post(f'{API_URL}/anomaly', json={'threshold': float(thr)}, timeout=20)
            data = r.json()
            mean = data.get('mean')
            std = data.get('std')
            anomalies = pd.DataFrame(data.get('anomalies', []))

            # local timeseries for plotting
            ts_local = df.groupby('date')['revenue'].sum().reset_index()
            ts_local = ts_local.sort_values('date')

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=ts_local['date'], y=ts_local['revenue'], mode='lines', name='Revenue', line=dict(color='#0b3d91')))

            if mean is not None and std is not None:
                upper = mean + float(thr) * std
                lower = mean - float(thr) * std
                fig.add_hline(y=mean, line_dash='dash', line_color='green', annotation_text=f'Mean: {mean}', annotation_position='top left')
                fig.add_hline(y=upper, line_dash='dot', line_color='red', annotation_text=f'Upper ({thr}σ): {round(upper,2)}', annotation_position='top right')
                fig.add_hline(y=lower, line_dash='dot', line_color='red', annotation_text=f'Lower ({thr}σ): {round(lower,2)}', annotation_position='bottom right')

            if not anomalies.empty:
                anomalies['date'] = pd.to_datetime(anomalies['date'])
                fig.add_trace(go.Scatter(x=anomalies['date'], y=anomalies['revenue'], mode='markers', name='Anomalies', marker=dict(color='red', size=10, symbol='x')))

                fig.update_layout(margin=dict(l=10,r=10,t=40,b=10), template='plotly_dark' if st.session_state.theme=='dark' else 'plotly_white', title='Revenue with Anomalies', xaxis_title='Date', yaxis_title='Revenue')
            st.plotly_chart(fig, use_container_width=True)

            st.markdown('**Anomalies (table)**')
            if anomalies.empty:
                st.info('No anomalies detected at this threshold.')
            else:
                st.dataframe(anomalies)

        except Exception as e:
            st.error('API call failed: ' + str(e))

else:
    st.markdown("""
    ### About InsightX PRO
    - Demo product for forecasting, segmentation, and anomaly detection.
    - Use `training/train_models.py` to create segmentation.joblib
    - API endpoints: /forecast, /segment, /anomaly
    """)
