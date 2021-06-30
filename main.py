from flask import Flask, render_template, request
import markovify
import re
import spacy
from forms import BoldifyEncryptForm
from markupsafe import Markup
from flask_ckeditor import CKEditor

nlp = spacy.load("en_core_web_sm")

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

def getPara():
  with open('data.txt','r', encoding='utf-8') as f:
      text = f.read()

  text_model = markovify.Text(text)
  paragraph = " "
  counter = 0
  sentencesUsed = []
  while counter < 20:
    output = text_model.make_sentence()
    if isinstance(output, str):
      if output not in sentencesUsed:
        sentencesUsed.append(output)
        paragraph += output + " "
        counter += 1
  return paragraph

def boldify(msg):
  limit = 10
  counter = 0
  while limit >= counter:
    paragraph = getPara()
    boldifiedText=[]
    remainingText=[i for i in paragraph]
    error = False
    for letter in msg:
      lowerIndex = None
      upperIndex = None
      try:
        lowerIndex = remainingText.index(letter)
      except:
        print("No Lower Index")
      try:
        upperIndex = remainingText.index(letter.upper())
      except:
        print("No Upper Index")
      index = None
      if lowerIndex == None and upperIndex == None:
        error = True
        break
      elif lowerIndex != None and upperIndex == None:
        index = lowerIndex
      elif lowerIndex == None and upperIndex != None:
        index = upperIndex
      else:
        index = min(lowerIndex, upperIndex)
      remainingText[index] = '<b>'+remainingText[index]+'</b>'
      boldifiedText += remainingText[:index+1]
      remainingText = remainingText[index+1:]
    try:
      periodIndex = min([remainingText.index(i) for i in ['.', ';', '!', '?']]) 
      boldifiedText += remainingText[:periodIndex+1]
    except:
      boldifiedText += remainingText
    if not error:
      return Markup(''.join(boldifiedText).replace('\n', ''))
    counter += 1
  return None

application = Flask('Boldify')
application.config['SECRET_KEY'] = '7b7e30111ddc1f8a5b1d80934d336798'
application.config['CKEDITOR_PKG_TYPE'] = 'basic'
ckeditor = CKEditor(application)

@application.route('/', methods=['GET', 'POST'])
@application.route('/', methods=['GET', 'POST'])
def homepage():
  return render_template('homepage.html')

@application.route('/encode', methods=['GET', 'POST'])
def boldifyEncoder():
  submitted = False
  form = BoldifyEncryptForm()
  output = None
  if form.validate_on_submit():
    submitted=True
    msg=str(request.form['boldMessage']).lower()
    msg=''.join([i for i in msg if i.isalpha()])
    output=boldify(msg)
  return render_template('boldifyencoder.html', form=form, submitted=submitted, output=output)

@application.route('/decode', methods=['GET', 'POST'])
def boldifyDecoder():
  submitted=False
  decodedMessage = ''
  if request.method == 'POST':
    submitted=True
    richText = request.form.get('ckeditor')
    richText = richText[3:len(richText)-6]
    iterator = re.finditer("<strong>", richText)
    for i in iterator:
      decodedMessage += richText[i.span()[1]]
  return render_template('boldifydecoder.html', submitted=submitted, decodedMessage=decodedMessage)

application.run(host='0.0.0.0', port=8080)
