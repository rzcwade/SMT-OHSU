import os
import subprocess
import yaml
 

def translate(text):
    """
    Run translation model using config
    """
    with open('/home/ren/run_moses/config.yaml', 'r') as f:
        doc = yaml.load(f)
    fileIn = doc['sample-models']['in']
    fileOut = doc['sample-models']['out']
    homeDir = doc['sample-models']['homeDir']
    runCommand = doc['sample-models']['command']
    # subprocess.call to capture the output
    subprocess.call(['rm %s && rm %s' % (fileIn, fileOut)], shell=True)
    text8 = text.encode('utf8')
    inputFile = open(fileIn, 'w')
    inputFile.write(text8 + '\n')
    #inputFile.write(str(text8))
    inputFile.close()
    subprocess.call([runCommand], cwd=homeDir, shell=True)
    readTranslate = open(fileOut, 'r')
    translatedText = readTranslate.read().decode('utf8')
    #translatedText = readTranslate.read()
    readTranslate.close()
    return translatedText.encode('utf8').rstrip()
    #return translatedText.rstrip()

def upload(file):
    """
    Tranlsate file
    """
    
    if os.stat(file).st_size != 0:
        with open(file,'r') as f:
            text = f.read().decode('utf8')
            #text = f.read()
            text = translate(text)
        f_out = open('output.txt', 'w')
        f_out.write(text)
        #f_out.write(str(text))
    else:
        return ('Error reading file...\n')
        #print('error')


#upload('input.txt')
