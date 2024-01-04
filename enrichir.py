import sys
import os
import re
import codecs

#recuperer les noms des medicaments apartir du fichier subst.dic
def recuperer_subst_dic(subst_dic_path):
    subst_dic = {}
    with codecs.open(subst_dic_path, 'r', encoding='UTF-16LE') as file:
        for line in file:
            key, value = line.strip().split(',',1)
            subst_dic[key] = value
    return subst_dic
    
#extraire les noms de medicaments apartir de fichier corpus-medicale.txt
def extract_entite_medicale (corpus_medicale_path):
    with codecs.open(corpus_medicale_path, 'r', encoding='utf-8') as file:
        contenu = file.read()
    pattern = re.compile(r'(\b[A-Z][a-z]{4,}|[A-Z]{4,})\b (\d+\.\d+|\d+) (mg|g|ml|MG|G|ML)')
    matches = pattern.findall(contenu)
    entities = [match[0] for match in matches]
    return entities

#fonction pour sauvgarder le nouveau fichier subst.dic
def sauvgarder_subst_dic(subst_dic_path,subst_dic):
    with codecs.open(subst_dic_path,'w',encoding = 'UTF-16LE') as file:
        file.write('\ufeff')
        existing_keys = set()
        for key, value in sorted(subst_dic.items(), key=lambda x: x[0].lower()) :
            lower_key = key.lower()
            if lower_key not in existing_keys:
                file.write(f"{lower_key},{value}\n")
                existing_keys.add(lower_key)

#enrichir le dictionnaire subst.dic
def enrichir_subst_dic (subst_dic_path,corpus_medicale_path,subs_corpus_path,info2_path,info3_path):
    subst_dic = recuperer_subst_dic(subst_dic_path)
    entities = extract_entite_medicale(corpus_medicale_path)
    with codecs.open(subs_corpus_path,'w',encoding = 'UTF-16LE') as file:
        file.write('\ufeff')
        
        for entity in entities:
            entity = entity.lower()
            #generer le fichier subs-corpus.dic

            file.write(f"{entity},.N+subst\n")
            subst_dic[entity] = '.N+subst'

    sauvgarder_subst_dic(subst_dic_path, subst_dic)        

    #generer le fichier info2.txt
    entities_sans_doublons = []
    for entity in entities:
        if entity not in entities_sans_doublons:
            entities_sans_doublons.append(entity)
    with codecs.open(info2_path,'w', encoding = 'utf-8') as file:
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            count = sum(1 for entity in entities_sans_doublons if entity.lower().startswith(letter) )
            file.write(f"{letter.upper()}: {count} entite\n")
        file.write(f"Totale: {len(entities) } entite\n")

    #generer le fichier info3.txt
    subst_dic_sans_doublons = {}
    with codecs.open(subst_dic_path,'r',encoding = 'UTF-16LE') as file:
        for line in file:
            key, value  = line.strip().split(',',1)
            if key not in subst_dic_sans_doublons :
                subst_dic_sans_doublons[key] = value
    with codecs.open(info3_path,'w', encoding = 'utf-8') as file:
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            count = sum(1 for key in subst_dic_sans_doublons if key.lower().startswith(letter))
            file.write(f"{letter.upper()} : {count}entite\n")
        file.write(f"Totale: {len(subst_dic_sans_doublons)}entite\n")


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python enrichir.py subst_dic_path corpus_medicale_path subs_corpus_path info2_path info3_path")
        sys.exit(1)

    subst_dic_path, corpus_medicale_path, subs_corpus_path, info2_path, info3_path = sys.argv[1:]

    enrichir_subst_dic(subst_dic_path, corpus_medicale_path, subs_corpus_path, info2_path, info3_path)
