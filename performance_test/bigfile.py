from mediawiki_parser import html, raw
import tmp_preprocessor as preprocessor
from pijnu.library.pattern import Pattern
import cProfile, pstats
from glob import glob
import os
import json
from multiprocessing import Pool, Manager
import time

foo = ""
def testit(content):
    global foo
    templates = {}
    allowed_tags = ["PRE"]
    allowed_self_closing_tags = []
    allowed_attributes = []
    interwiki = {}
    namespaces = {}

    preprocess = preprocessor.make_parser(templates)

    parser = html.make_parser(allowed_tags, allowed_self_closing_tags, allowed_attributes, interwiki, namespaces)
    #parser._setTopPattern('wikitext')

    #parser = raw.make_parser()

    preprocessed_text = preprocess.parseTest(content)
    #import pdb; pdb.set_trace()
    #Pattern.TRACE=True
    foo = parser.parseTest(preprocessed_text).leaves()
    #return preprocessed_text.treeView()


def custom_parser( d ):
   
    content = ""
    try:
        os.mkdir(os.path.join( '/','data','kowiki','wikiextractor','html',d.split('/')[-1]) )
    except FileExistsError:
        pass

    for doc in glob(d + '/wiki*'):
        print(doc)
        with open( doc, 'r') as f:
            for doc_json in f:
                try:
                    cnt = json.loads(doc_json)
                    if '#넘겨주기' in cnt['text'] : continue
                    content = cnt['text']#open(doc, "r").read()
                    testit(content)
                    '''
                    cProfile.run('testit(content)', 'results')
                    results = pstats.Stats('results')
                    results.strip_dirs()
                    results.sort_stats('time')
                    results.print_stats()
                    results.print_callers('pattern.py', .2)
                    '''
                    fname = cnt['title']+'.html'
                    outpath = os.path.join( '/','data','kowiki', 'wikiextractor', 'html',d.split('/')[-1], fname)
                    f = open(outpath, "w+")
                    f.truncate()
                    f.write( foo )
                    print( outpath , 'is converted')
                except BaseException as e:
                    print( doc, ':' , e)
                    print(content[:20])
                    continue 


if __name__ == "__main__":
    st = time.time()
    pool = Pool(processes=6)
    m = Manager()
    dir_ = glob('/data/kowiki/wikiextractor/text/*')
    print(dir_)

    pool.map( custom_parser, dir_ )
    pool.close()

    print( '--- %s sec ---' % (time.time() - st) )

    


