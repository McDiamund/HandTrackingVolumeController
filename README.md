# Hand Tracking Volume Slider

This project allows fora user to press their index finger to their thumb and slide left or right to control the volume on their windows computer. It uses google Mediapipe to make these 
quick inferrences of movement. 

Each finger is tracked and the distance between them all (with math) is compared to a threshold. When that threshold is met a sequence activated where any movement left or right occurs 
it reduces or increases respectively. 

This is made in python.
