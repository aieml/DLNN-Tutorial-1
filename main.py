import re
import base64
from flask import Flask, render_template,request

app = Flask(__name__)

@app.route('/')
def index():
    global draw_digit
    draw_digit=0
    return render_template('drawdigits.html')

@app.route('/predictdigits/', methods=['GET','POST'])
def predict_digits():
    parseImage(request.get_data())
    return "DONE"

def crop(im):

    ret,thresh1 = cv2.threshold(im,127,255,cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    i=0
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        #following if statement is to ignore the noises and save the images which are of normal size(character)
        #In order to write more general code, than specifying the dimensions as 100,
        # number of characters should be divided by word dimension            
        if(i==1):
            return thresh1[y:y+h,x:x+w]
        i=i+1

def parseImage(imgData):
    # parse canvas bytes and save as output.png
    imgstr = re.search(b'base64,(.*)', imgData).group(1)
    with open('output.png','wb') as output:
        output.write(base64.decodebytes(imgstr))

if __name__ == '__main__':
    app.run(debug=True)
