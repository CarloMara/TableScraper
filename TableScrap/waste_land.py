def processframe():
    img = cv2.imread('../p215.png')
    img = cv2.resize(img, (W, H))

    edges = cv2.Canny(img,275,500, apertureSize=3)

    # for i in range(100, 200):
    lines = cv2.HoughLines(edges,1,np.pi/270,125)

    for line in lines:
        for rho,theta in line:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),1)
    return [img, edges]

def check_collision(bigger, smaller):
    if bigger[0] > smaller[0] and bigger[1] < smaller[1] and bigger[2] < smaller[2] and bigger[3] > smaller[3]:
        return True
    return False
