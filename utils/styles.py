"""
Unified Styling System for InsightX Exchange
Consistent design patterns across all pages
"""

def get_global_styles():
    """Return global CSS styles for consistent design"""
    return """
    <style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    /* Enhanced Header Styles */
    .page-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .page-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 20px 20px;
        opacity: 0.3;
        animation: float 20s linear infinite;
    }
    
    @keyframes float {
        0% { transform: translate(0, 0) rotate(0deg); }
        100% { transform: translate(10px, 10px) rotate(360deg); }
    }
    
    .page-header h1 {
        color: white;
        margin: 0;
        font-size: 2.8em;
        font-weight: 700;
        text-shadow: 0 4px 15px rgba(0,0,0,0.2);
        position: relative;
        z-index: 2;
    }
    
    .page-header p {
        color: rgba(255,255,255,0.95);
        margin: 10px 0 0 0;
        font-size: 1.2em;
        position: relative;
        z-index: 2;
    }
    
    /* Card Styles */
    .card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }
    
    .card-primary {
        border-left: 4px solid #667eea;
    }
    
    .card-secondary {
        border-left: 4px solid #764ba2;
    }
    
    .card-success {
        border-left: 4px solid #28a745;
    }
    
    .card-warning {
        border-left: 4px solid #ffc107;
    }
    
    .card-danger {
        border-left: 4px solid #dc3545;
    }
    
    .card-info {
        border-left: 4px solid #17a2b8;
    }
    
    /* Feature Card Styles */
    .feature-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transition: left 0.6s ease;
    }
    
    .feature-card:hover::before {
        left: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .feature-icon {
        font-size: 48px;
        margin-bottom: 15px;
        display: block;
    }
    
    .feature-title {
        color: #667eea;
        font-size: 1.3em;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .feature-description {
        color: #666;
        line-height: 1.6;
    }
    
    /* Status Indicators */
    .status-success {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 10px 15px;
        border-radius: 8px;
        font-weight: 500;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 10px 15px;
        border-radius: 8px;
        font-weight: 500;
    }
    
    .status-error {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 10px 15px;
        border-radius: 8px;
        font-weight: 500;
    }
    
    /* Enhanced Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
        margin: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        border: 2px solid #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
    
    .fade-in {
        animation: fadeIn 0.8s ease-out;
    }
    
    .slide-in {
        animation: slideIn 0.5s ease-out;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .page-header h1 {
            font-size: 2.2em;
        }
        
        .page-header p {
            font-size: 1.1em;
        }
        
        .feature-grid {
            grid-template-columns: 1fr;
        }
        
        .card {
            padding: 20px;
        }
    }
    
    /* Hide default Streamlit elements */
    .stApp > footer {
        display: none;
    }
    
    .main .block-container {
        padding-top: 30px !important;
        padding-bottom: 30px !important;
    }
    </style>
    """

def get_page_header(title: str, subtitle: str, icon: str = "📊"):
    """Generate consistent page header"""
    return f"""
    <div class="page-header">
        <h1>{icon} {title}</h1>
        <p>{subtitle}</p>
    </div>
    """

def get_card(title: str, content: str, card_type: str = "primary", icon: str = ""):
    """Generate consistent card component"""
    return f"""
    <div class="card card-{card_type} fade-in-up">
        <h3 style="color: #667eea; margin-bottom: 15px;">
            {icon} {title}
        </h3>
        <div style="color: #666; line-height: 1.6;">
            {content}
        </div>
    </div>
    """

def get_info_box(title: str, content: str, icon: str = "ℹ️"):
    """Generate consistent info box"""
    return f"""
    <div class="info-box slide-in">
        <h3 style="color: #667eea; margin-bottom: 15px;">
            {icon} {title}
        </h3>
        <div style="color: #666; margin: 0;">
            {content}
        </div>
    </div>
    """

def get_feature_card(icon: str, title: str, description: str):
    """Generate feature card for grid layouts"""
    return f"""
    <div class="feature-card fade-in-up">
        <span class="feature-icon">{icon}</span>
        <div class="feature-title">{title}</div>
        <div class="feature-description">{description}</div>
    </div>
    """

def get_status_message(message: str, status_type: str = "success"):
    """Generate status message"""
    return f"""
    <div class="status-{status_type}">
        {message}
    </div>
    """
