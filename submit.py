# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 12:22:41 2017

@author: zicheng
"""

from flask import Flask, redirect, url_for, request, render_template
import moses_translate
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('translate.html')


@app.route('/success')
def success():
    return render_template('save_res.html')

@app.route('/translation_res',methods=['POST','GET'])
def translation_res():
   if request.method == 'POST':
      if request.form['submit']=='Do the thing':
          return redirect(url_for('success'))

@app.route('/translate',methods = ['POST','GET'])
def translate():
   if request.method == 'POST':
      text_input = request.form['textline']
      text_in = text_input.lower()
      with open('input.txt','w') as f_in:
          f_in.write(text_in)
      # get translate function from run_me module to initiate moses translation
      moses_translate.upload('input.txt')
      with open('output.txt','r') as f_out:
          text_out = f_out.read()
      os.system('python2 ir_part.py')
    
      #if request.form['submit'] == 'Do the thing' and os.stat("input.txt").st_size != 0:
      #return redirect(url_for('translation_res')), text_in, text_out
      #sub_input = process_text
      #sub_output =  text_out
      return render_template('translation_res.html', sub_input=text_in, sub_output=text_out)
      #return sub_input, sub_output
