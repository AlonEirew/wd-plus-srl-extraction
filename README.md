# ecb-wd-plus-srl-extraction
Different methods for extracting Within-Document(WD) and Semantic-Role-Labeling(SRL) information from ECB+ corpus

Overview
--
####Current Implementations:
- *AllenNLP Coreference Resolution:* For extracting within document coreference from ECB+ corpus and align mentions
- *AllenNLP Semantic Role Labeling:* For extracting SRL relations from ECB+ corpus and align mentions and tokens

Pre-Requirements
--
- Python 3.6 or higher
- allennlp
- ECB+ corpus root folder named 'ECB+' (<a href="http://www.newsreader-project.eu/results/data/the-ecb-corpus/">Download ECB+</a>)


Run
--
- ``coref_allen.py``  Generate within document co-reference using AllenNLP


    python src/coref_allen.py --ecb_root_path=ECB+ --output_file=output/allen_wd_coref.json

- ``srl_allen.py`` Generate semantic role labeling using AllenNLP


    python src/srl_allen.py --ecb_root_path=ECB+/1 --output_file=output/allen_srl.json

In order to read the json file back to objects use ``srl_allen.read_srl_json(input_file)`` method
