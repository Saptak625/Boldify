from flask import Flask, render_template, flash, request
import markovify
import re
import nltk
from nltk.tag import pos_tag
from forms import BoldifyEncryptForm
from markupsafe import Markup
from flask_ckeditor import CKEditor

class POSifiedText(markovify.Text):
  def word_split(self, sentence):
    words = nltk.word_tokenize(sentence)
    tagged = pos_tag(words)
    return tagged

  def word_join(self, words):
    sentence = " ".join([word[0] for word in words])
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
        pass
      try:
        upperIndex = remainingText.index(letter.upper())
      except:
        pass
      index = None
      if lowerIndex == None and upperIndex == None:
        error = True
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
      boldifiedText = ''.join(boldifiedText).replace('\n', '').replace('  ', ' ')
      sentences = boldifiedText.split('. ')
      shortenedText = '. '.join([i for i in sentences if '</b>' in i])
      return Markup(f'{shortenedText}.')
    counter += 1
  raise Exception('Letter not found in remaining text. Please try again or shorten your message.')

app = Flask('Boldify')
app.config['SECRET_KEY'] = '7b7e30111ddc1f8a5b1d80934d336798'
app.config['CKEDITOR_PKG_TYPE'] = 'basic'
ckeditor = CKEditor(app)

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def homepage():
  return render_template('homepage.html', data=None)

@app.route('/encode', methods=['GET', 'POST'])
def boldifyEncoder():
  data = None
  form = BoldifyEncryptForm()
  if form.validate_on_submit():
    msg=str(request.form['boldMessage']).lower()
    msg=''.join([i for i in msg if i.isalpha()])
    try:
      data=boldify(msg)
    except:
      print('Exception raised')
      flash('Letter not found in remaining text. Please try again or shorten your message.', 'error')
  return render_template('boldifyencoder.html', form=form, data=data)

@app.route('/decode', methods=['GET', 'POST'])
def boldifyDecoder():
  data = None
  if request.method == 'POST':
    data = ""
    richText = request.form.get('ckeditor')
    richText = richText[3:len(richText)-6]
    iterator = re.finditer("<strong>", richText)
    for i in iterator:
      if richText[i.span()[1]]:
        data += richText[i.span()[1]]
    data = data.lower()
  return render_template('boldifydecoder.html', data=data)

if __name__ == "__main__":
    #Development only
    app.run(debug=True)
