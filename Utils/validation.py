
def phone_no_validation(phone_no):
    cleaned_phone_no = phone_no.replace("-","").replace(" ", "").strip()
    if cleaned_phone_no.isdigit() and len(cleaned_phone_no)==10:
        return True
    return False


def email_validation(email):
    cleaned_email = email.strip()
    if cleaned_email.count("@")==1 and "." in cleaned_email:
        return True
    return False


def student_form_validation(data):

    errors = []

    if not data.get("name", ""):
        errors.append("Name is required")


    email = data.get("email","")
    if not email:
        errors.append("Email is required")
    else:
        if not email_validation(email):
            errors.append("This Email is Invalid")


    phone_no = data.get("phone_no", "")
    if not phone_no:
        errors.append("Phone No. is required")
    else:
        if not phone_no_validation(phone_no):
            errors.append("This Phone no. is Invalid")


    if not data.get("gender", ""):
        errors.append("Gender is required")

    if not data.get("dob", ""):
        errors.append("Dob is required")

    if not data.get("fatherName", ""):
        errors.append("Father's Name is required")


    fatherPhone_no = data.get("fatherPhone_no", "")
    if not fatherPhone_no:
        errors.append("Father's Phone No. is required")
    else:
        if not phone_no_validation(fatherPhone_no):
            errors.append("This Father's Phone No. is Invalid")
    
    if not data.get("local_address", ""):
        errors.append("Local address is required")

    if not data.get("permanent_address", ""):
        errors.append("Permanent address is required")

    if not data.get("aadhaar_front", ""):
        errors.append("Aadhaar front is required")
    
    if not data.get("aadhaar_back", ""):
        errors.append("Aadhaar back is required")


    if data.get("profile", "") == "Student":
        if not data.get("qualification", ""):
            errors.append("Qualification is required")

        if not data.get("passing_year", ""):
            errors.append("Passing year is required")

        if not data.get("collage_name", ""):
            errors.append("Collage name is required")

    elif data.get("profile", "") == "Working Professional":
        if not data.get("highest_qualification", ""):
            errors.append("Highest Qualification is required")
          
        if not data.get("company_name", ""):
            errors.append("Company name is required")

        if not data.get("years_of_experience", ""):
            errors.append("Years of experience is required")


    if not data.get("course" ""):
        errors.append("Select a Course")


    if not data.get("terms" ""):
        errors.append("Please Agree to our terms and conditions")

    if len(errors)==0:
        is_valid = True
    else:
        is_valid = False

    return is_valid, errors
    

    
    
    
    
    
    

    
    
