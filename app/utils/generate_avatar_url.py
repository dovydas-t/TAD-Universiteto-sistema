import random

def generate_avatar_url(username, email=None):
    """Generate a default avatar URL based on username or email"""
    # Use email if provided, otherwise use username
    if email:
        name = email.split('@')[0]
    else:
        name = username
    
    # Random background colors
    colors = ['3498db', 'e74c3c', '2ecc71', 'f39c12', '9b59b6', '1abc9c', 'e67e22', '34495e']
    bg_color = random.choice(colors)
    
    # Generate URL using UI Avatars service
    return f"https://ui-avatars.com/api/?name={name}&background={bg_color}&color=fff&size=200&bold=true"