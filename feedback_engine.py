def generate_feedback(coding, hours, projects, attendance, domain=None):

    feedback = ""

    if coding < 3:
        feedback += "The student needs to improve programming fundamentals and practice coding regularly. "
    else:
        feedback += "The student demonstrates good coding skills. "

    if projects < 2:
        feedback += "More practical projects should be completed to gain hands-on experience. "
    else:
        feedback += "The student has shown initiative in completing practical projects. "

    if hours < 10:
        feedback += "Increasing weekly learning hours will help build deeper technical knowledge. "

    if attendance < 75:
        feedback += "Regular participation in internship activities is recommended. "

    # Domain suggestion
    if domain:
        if domain.lower() == "ml":
            feedback += "Focus more on model training, data preprocessing, and evaluation metrics. "
        elif domain.lower() == "ai":
            feedback += "Practice artificial intelligence concepts like NLP and deep learning. "
        elif domain.lower() == "frontend":
            feedback += "Improve UI development using HTML, CSS, and JavaScript frameworks. "
        elif domain.lower() == "backend":
            feedback += "Strengthen backend skills using APIs, databases, and server logic. "

    return feedback