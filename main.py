from flask import Flask,render_template


app=Flask(__name__)

@app.route('/main',methods=['GET','POST'])
def main():
    return render_template('helloworld.html')

if __name__ =="__main__":
    app.run()