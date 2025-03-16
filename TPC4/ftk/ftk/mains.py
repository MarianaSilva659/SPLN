import jjcli
import json
from ftk.base import Pipeline, Convert2ProbabilityStage
from ftk.probability import RelativeProbabilityPerMillion
from ftk.corpus import get_dictionary, languages


def pretty_print(freqs, opts):
    freqs = dict(sorted(freqs.items(), key=lambda item: item[1].value, reverse=True))
    total = freqs[list(freqs.keys())[0]].total

    if '-a' not in opts:
        freqs = {key: RelativeProbabilityPerMillion(val) for key, val in freqs.items()}

    if '-m' in opts:
        m = int(opts['-m'])
        freqs = dict(list(freqs.items())[:m])

    freqs = {key: val.value for key, val in freqs.items()}
    if '-j' in opts:
        print(json.dumps({'total': total, 'words': freqs}, indent=4))
    else:
        print(total)
        for key, val in freqs.items():
            print(f'{val}\t{key}')
    
def main():
    """Options:
        -a: aboslute frequency
        -m N: top N words
        -j: JSON output
    """

    cl = jjcli.clfilter("am:j", doc=main.__doc__)
    pipe = Pipeline()
    pipe.set_reduction(Convert2ProbabilityStage())

    for txt in cl.text():
        c = pipe.apply(txt)
        pretty_print(c, cl.opt)


if __name__ == '__main__':
    main()


#TODO subtrair as freqs  novo/freq
def main_surpresa():
    """Options:
        -l: language identifier (default: pt)
    """
    # vamos comparar o texto mandado no terminal com o dicionárfio
    cl = jjcli.clfilter("l:", doc=main_surpresa.__doc__)
    
    dic_geral = get_dictionary(cl.opt.get('-l', 'pt'))
    pipe = Pipeline()
    pipe.set_reduction(Convert2ProbabilityStage())
    # devolve as probabilidades absolutas
    for txt in cl.text():
        txt_abs_freq = pipe.apply(txt)

        racios = []
        
        for word, freq in txt_abs_freq.items():
            freq_value = (freq.value) 
            dic_value = (dic_geral.get(word, 2).value)  

            print("freq", freq_value)
            print("dic", dic_value)

            if dic_value != 0:  
                ratio = freq_value / dic_value
            else:
                ratio = 0

            print("freq/dic", ratio)
            racios.append((ratio, word))

         
        print(racios)   
        #print(sorted(lambda v: v[0].valeu, racios))
                
                