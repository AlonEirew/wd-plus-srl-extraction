# wd-plus-srl-extraction
Different methods for extracting Within-Document(WD) and Semantic-Role-Labeling(SRL) information already tokenized corpus, then align the extracted information

Include implementation for extracting from ECB+ corpus

Overview
--

#### Current Implementations:

- *AllenNLP Coreference Resolution:* For extracting AllenNLP within document coreference
- *AllenNLP Semantic Role Labeling:* For extracting AllenNLP SRL relations 
- *SpaCy Coreference Resolution:* For extracting SpaCy within document coreference

Pre-Requirements
--
- Python 3.6 or higher
- allennlp *(Code here uses methods that might not have been released yet by AllenNLP, there might be a need to checkout AllenNLP latest and build locally)*
- spacy
- Download Within doc SpaCy model from <a href="https://github.com/huggingface/neuralcoref">neuralcoref</a>
- if running ECB+ corpus, download from (<a href="http://www.newsreader-project.eu/results/data/the-ecb-corpus/">Download ECB+</a>)

Install
--

    pip install -r requirements.txt

Run
--
- `coref_allen.py` Generate within document co-reference using AllenNLP


    python src/coref_allen.py --ecb_root_path=ECB+ --output_file=output/allen_wd_coref.json

- `srl_allen.py` Generate semantic role labeling using AllenNLP


    python src/srl_allen.py --ecb_root_path=ECB+/1 --output_file=output/allen_srl.json

- In order to read the json file back to objects use ``srl_allen.read_srl_json(input_file)`` method

- `coref_spacy.py` Generate within document co-reference using neuralcoref


    python src/coref_spacy.py --ecb_root_path=ECB+ --output_file=output/spacy_wd_coref.json --model=en_coref_lg
    

Experiment with other corpus
--
* Clone the repo
* Inherit `IDataLoader` and create a new `DataLoader` for parsing your corpus (see `EcbDataLoader` for example)
* replace `DataLoader` in required model `main()` method


Output
--
Output is in a json format, containing a list of within document coreference mentions:

    [
        {
            "coref_chain": "0",
            "doc_id": "36_5ecb.xml",
            "sent_id": 4,
            "tokens_number": [
                1,
                2
            ],
            "tokens_str": "Mr. Blackmore"
        },
        {
            "coref_chain": "0",
            "doc_id": "36_5ecb.xml",
            "sent_id": 4,
            "tokens_number": [
                7
            ],
            "tokens_str": "he"
        },
        .
        .
        .
    ]
    
#### Where:
  
| json field  | Value | comment |
| ------------- | ------------- | ------------- |
| coref_chain | Text | The mention coref cluster id |
| doc_id | Text | the document this mention belong to |
| sent_id | int | Mention original document sentence ID |
| tokens_number | List[int] | Mention span (text phrase as set in tokens_str) original tokens ids |
| tokens_str | String | The mention/span phrase |
