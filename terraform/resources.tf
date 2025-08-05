resource "aws_instance" "weather-app-server1" {
    ami = "ami-020cba7c55df1f615"
    instance_type = "t2.micro"

    tags = {
        Name = "Weather-App-Server"
    }
  
}