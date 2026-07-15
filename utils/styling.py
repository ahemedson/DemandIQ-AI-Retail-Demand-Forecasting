import os
import streamlit as st
import plotly.graph_objects as go
import streamlit.components.v1 as components


def apply_custom_styling(dark_mode=False):
    """
    Load custom CSS and inject brand assets (SVG logo) into the sidebar.
    """
    # 1. Inject CSS
    css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

    # 2. Inject Dark Theme Overrides dynamically in Python if active
    if dark_mode:
        dark_theme_css = """
        <style>
        [data-testid="stAppViewContainer"], [data-testid="stSidebar"], body, html {
            --bg-color: #090D16 !important;
            --text-color: #F1F5F9 !important;
            --heading-color: #00B4D8 !important;
            --subheading-color: #CBD5E1 !important;
            --muted-color: #94A3B8 !important;
            
            --card-bg: #131B2E !important;
            --card-border: #1E293B !important;
            --card-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -2px rgba(0, 0, 0, 0.2) !important;
            --card-hover-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4), 0 4px 6px -4px rgba(0, 0, 0, 0.4) !important;
            
            --sidebar-bg: linear-gradient(180deg, #05080E 0%, #0B1221 100%) !important;
            --sidebar-border: #131B2E !important;
            --sidebar-text: #94A3B8 !important;
            --sidebar-nav-text: #64748B !important;
            --sidebar-active-bg: rgba(0, 180, 216, 0.2) !important;
            --sidebar-active-border: rgba(0, 180, 216, 0.4) !important;
            --sidebar-active-accent: #00B4D8 !important;
            
            --input-bg: #0F172A !important;
            --input-border: #1E293B !important;
            --input-text: #F1F5F9 !important;
            
            --chat-user-bg: #0C111D !important;
            --chat-assistant-bg: #131B2E !important;
            --chat-user-border: #00B4D8 !important;
            --chat-assistant-border: #06D6A0 !important;
        }
        </style>
        """
        st.markdown(dark_theme_css, unsafe_allow_html=True)

    # 3. Render SVG Logo Header in Sidebar
    logo_svg = """
    <div style="text-align: center; margin-bottom: 25px; padding: 10px 0;">
        <svg width="90" height="90" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" style="display: block; margin: 0 auto;">
            <!-- Stylized D Outer Shape -->
            <path d="M25 15 H55 C74 15 88 28 88 50 C88 72 74 85 55 85 H25 V15 Z" fill="#0B2545"/>
            <!-- Inner cutout of D -->
            <path d="M38 25 V75 H53 C66 75 75 66 75 50 C75 34 66 25 53 25 H38 Z" fill="#081225"/>
            <!-- Upward Growth Bars -->
            <rect x="40" y="58" width="6" height="17" rx="1.5" fill="#0077B6" />
            <rect x="48" y="48" width="6" height="27" rx="1.5" fill="#00B4D8" />
            <rect x="56" y="38" width="6" height="37" rx="1.5" fill="#06D6A0" />
            <rect x="64" y="26" width="6" height="49" rx="1.5" fill="#38B000" />
            <!-- Sweeping White Arrow Line -->
            <path d="M28 78 C40 74 56 64 78 40" stroke="#FFFFFF" stroke-width="4.5" stroke-linecap="round" fill="none"/>
            <path d="M78 40 L69 41 M78 40 L76 49" stroke="#FFFFFF" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        </svg>
        <div style="font-size: 1.7rem; font-weight: 700; color: #FFFFFF; margin-top: 12px; font-family: 'Inter', sans-serif; letter-spacing: -0.5px;">
            Demand<span style="background: linear-gradient(135deg, #00B4D8, #06D6A0); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">IQ</span>
        </div>
        <div style="font-size: 0.65rem; letter-spacing: 0.18em; color: #94A3B8; font-weight: 600; text-transform: uppercase; margin-top: 6px; display: flex; align-items: center; justify-content: center; gap: 6px;">
            <span style="height: 1px; width: 12px; background-color: #00B4D8; display: inline-block;"></span>
            Insight. Forecast. Grow.
            <span style="height: 1px; width: 12px; background-color: #06D6A0; display: inline-block;"></span>
        </div>
    </div>
    """
    st.sidebar.markdown(logo_svg, unsafe_allow_html=True)


def style_plotly_figure(fig: go.Figure) -> go.Figure:
    """
    Apply global premium enterprise-grade styling to any Plotly figure.
    - Uses fonts from the design system
    - Maps colors to brand guidelines (Navy, Teal, Green)
    - Clarifies margins, legends, and gridlines
    """
    if fig is None:
        return None

    # Custom palette definitions
    navy = '#0B2545'
    teal = '#00B4D8'
    green = '#06D6A0'
    light_blue = '#E0F2FE'
    slate_subtle = '#64748B'
    grid_color = 'rgba(148, 163, 184, 0.08)'

    # 1. Update data/traces styling
    for trace in fig.data:
        # Check trace type and apply colors
        if trace.type == 'bar':
            if not getattr(trace, 'marker', None):
                trace.marker = {}
            if getattr(trace, 'name', None) and 'Top' in trace.name:
                trace.marker.color = green
            elif getattr(trace, 'name', None) and 'Bottom' in trace.name:
                trace.marker.color = '#E63946'
            elif trace.name == "No Promotion":
                trace.marker.color = navy
            elif trace.name == "Promotion":
                trace.marker.color = teal
            else:
                trace.marker.color = teal
            trace.marker.line = dict(width=0)
            
        elif trace.type == 'scatter':
            if not getattr(trace, 'line', None):
                trace.line = {}
            trace.line.width = 3.5
            if trace.name == "Historical Sales":
                trace.line.color = navy
            elif trace.name == "Forecast":
                trace.line.color = teal
                trace.line.dash = 'dash'
            elif trace.name == "Remaining Inventory" or trace.name == "Remaining Stock":
                trace.line.color = green
                
            if getattr(trace, 'marker', None):
                trace.marker.size = 7
                trace.marker.line = dict(width=1.5, color='#FFFFFF')

        elif trace.type == 'histogram':
            if not getattr(trace, 'marker', None):
                trace.marker = {}
            trace.marker.color = teal
            trace.marker.line = dict(width=0.5, color='#FFFFFF')

    # 2. Update Layout
    fig.update_layout(
        template="plotly_white",
        font=dict(
            family="'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
            size=11,
            color="#64748B"
        ),
        title=dict(
            font=dict(
                size=15,
                color=teal,
                family="'Inter', sans-serif"
            ),
            pad=dict(b=10)
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=65, b=20),
        legend=dict(
            orientation="h",
            y=1.1,
            x=1,
            xanchor="right",
            font=dict(size=10, color=slate_subtle),
            bgcolor="rgba(255,255,255,0.05)"
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            linecolor="rgba(148, 163, 184, 0.2)",
            linewidth=1,
            tickfont=dict(size=10, color=slate_subtle),
            title=dict(font=dict(size=11, color=slate_subtle))
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            linecolor="rgba(148, 163, 184, 0.2)",
            linewidth=1,
            tickfont=dict(size=10, color=slate_subtle),
            title=dict(font=dict(size=11, color=slate_subtle))
        )
    )

    return fig
