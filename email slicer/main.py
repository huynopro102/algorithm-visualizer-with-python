from check_email import printMessage , emailProcess # nếu ko import thì nó sẽ chạy tất tần tật ở trong module của codexplore luôn cụ thể là main() đã đc gọi trong codexplore


def main():
   list_email=["khanhchua@gmail.com","nmopk123@gmail.com","jenkins123@dev.com","nginx-123@xh.com"]
   for email in list_email:
    email_username , email_domain = emailProcess(email=email)
    printMessage(email_username=email_username , email_domain=email_domain)
    print("\n")
   
   
   
if __name__ == "__main__":   
    main()