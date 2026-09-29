import streamlit as st
import datetime as dt
from Utils.validation import student_form_validation
from Utils.utils import save_uploaded_file
from Storage.mongodb_storage import register_student,init_db


# Initialize state
if "success" not in st.session_state:
    st.session_state.success = False

st.title("✏️ Registration Form")
    
if st.session_state.success == True:
    st.success("✅ Resistration successfull")
    if st.button("Register another student"):
        st.session_state.success = False
        st.rerun()


else:
    # container for **Personal Details** 
    with st.container(border=True):
        name = st.text_input("Full Name", placeholder="Enter your name")
        email = st.text_input("Email", placeholder="Enter Email")
        phone_no = st.text_input("Phone number", placeholder="10 digit")
        gender = st.selectbox("Gender",["Male", "Female", "Other"])
        dob = st.date_input("Date of Birth", format="DD/MM/YYYY", min_value=dt.datetime(1960,1,1), max_value="today", value=None)
        fatherName = st.text_input("Father's Name", placeholder="Enter Father's name")
        fatherPhone_no = st.text_input("Father's Phone number", placeholder="10 digit")

    # container for  **Address Details**
    with st.container(border=True):
        local_address = st.text_area("Local Address", key="local_address", placeholder="Enter your address")

        

        if st.checkbox("Same as Local Address"):
            permanent_address = st.text_area("Permanent Address", value=st.session_state.local_address, disabled=True)
        else:
            permanent_address = st.text_area("Permanent Address", placeholder="Enter your permanent adress")


    # container for **Aadhaar Verification**
    with st.container(border=True):
        col_f, col_back = st.columns(2)

        with col_f:
            aadhaar_front = st.file_uploader("Upload front of Aadhaar card", type="image", key="front", max_upload_size=5)
            if aadhaar_front:
                st.image(aadhaar_front)


        with col_back:
            aadhaar_back = st.file_uploader("Upload back of Aadhaar card", type="image", max_upload_size=5)
            if aadhaar_back:
                st.image(aadhaar_back)


    # container for **Professional Details**
    with st.container(border=True):
        profile = st.radio("profile", ["Student", "Working Professional"], key="profile", label_visibility="collapsed", horizontal=True)

        if profile == "Student":
            qualification = st.text_input("Qualification", placeholder="B.Tech, BCA, etc")
            passing_year = st.number_input("Passing Year", step=1, value=dt.datetime.now().year, min_value=dt.datetime.now().year-5)
            collage_name = st.text_input("Collage Name", placeholder="Enter collage name")


        elif profile == "Working Professional":
            highest_qualification = st.text_input("Highest Qualification", placeholder="B.Tech, BCA, etc")
            company_name = st.text_input("Company Name", placeholder="Enter company name")
            years_of_experience = st.number_input("Year of experience", step=1, min_value=0, max_value=60)


    # container for **Course Selection**
    with st.container(border=True):
        course = st.selectbox("Course", ["Full stack development", "Frontend development", "Backend development", "Python Mastry", "Data science", "Database management", "Dev-ops"], index=None, placeholder="Select Course")

    # container for **Referral**
    with st.container(border=True):
        referral = st.radio("Referral", ["Google / Search Engine","Social Media","Friend / Colleague","Blog / Article","Advertisement","Other"],horizontal=True)

    # container for **Terms**
    with st.container(border=True):
        terms = st.checkbox("Agree to Terms & Conditions")

    # container for **Submit button**
    with st.container():
        if st.button("Register"):
            # create payload for validation
            payload = {
                "name":name,
                "email":email,
                "phone_no":phone_no,
                "gender":gender,
                "dob":dob,
                "fatherName":fatherName,
                "fatherPhone_no":fatherPhone_no,
                "local_address":local_address,
                "permanent_address":permanent_address,
                "aadhaar_front":aadhaar_front,
                "aadhaar_back":aadhaar_back,
                "profile":profile,
                "qualification":qualification if profile=="Student" else None,
                "passing_year":passing_year if profile=="Student" else None,
                "collage_name":collage_name if profile=="Student" else None,
                "highest_qualification":highest_qualification if profile=="Working Professional" else None,
                "company_name":company_name if profile=="Working Professional" else None,
                "years_of_experience":years_of_experience if profile=="Working Professional" else None,
                "course":course,
                "referral":referral,
                "terms":terms
            }

            is_valid, errors = student_form_validation(payload)
            if is_valid:
                # Save to database
                front = save_uploaded_file(aadhaar_front,"front", phone_no)
                back = save_uploaded_file(aadhaar_back,"back", phone_no)

                data = {
                            "name":name,
                            "email":email,
                            "phone_no":phone_no,
                            "gender":gender,
                            "dob":dob.isoformat(),
                            "fatherName":fatherName,
                            "fatherPhone_no":fatherPhone_no,
                            "local_address":local_address,
                            "permanent_address":permanent_address,
                            "aadhaar_front":front,
                            "aadhaar_back":back,
                            "profile":profile,
                            "qualification":qualification if profile=="Student" else "",
                            "passing_year":passing_year if profile=="Student" else 0,
                            "collage_name":collage_name if profile=="Student" else "",
                            "highest_qualification":highest_qualification if profile=="Working Professional" else "",
                            "company_name":company_name if profile=="Working Professional" else "",
                            "years_of_experience":years_of_experience if profile=="Working Professional" else 0.0,
                            "course":course,
                            "referral":referral,
                            "terms":terms
                        }

                init_db()
                register_student(data)

                st.session_state.success = True
                st.rerun()

            
            else:
                for error in errors:
                    st.error(error)

        
