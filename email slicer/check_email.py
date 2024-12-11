def emailProcess(email : str) -> list:
    # huynguyen123@gmail.com
    email_username = email.split("@")[0]
    email_domain = email.split("@")[1]
    return [email_username,email_domain]

def printMessage(email_username : str , email_domain : str) -> None:
    print (f"Email_Domain is : {email_username} , Email_Domain is : {email_domain}")

def main():
    email = input("please enter your email address").strip()
    if "@" in email and "." in email:
        email_username , email_domain = emailProcess(email=email)
        printMessage(email_username=email_username,email_domain=email_domain)
    else:
        email = "huy123@gmail.com"
        print("Invalid email. Using default: huy123@gmail.com")
        email_username , email_domain = emailProcess(email=email)
        printMessage(email_username=email_username,email_domain=email_domain)

if __name__ == "__main__":
    main()    