# wd-plus-srl-extraction
This model was developed in order to extract SpaCy/AllenNLP `coref` and `SRL` from already tokenized corpus, 
in order to avoid aligning model output tokenization with corpus tokenization (which are usually different). 
im using the corpus tagged data (tokens, sentences,...) to create the tokenized data in the SpaCy format then feed to the SRL/coref model while skipping model tokenization pipeline.

Include implementation/example for extracting ECB+ corpus SRL/coref information

Overview
--

#### Current Implementations:

- *AllenNLP Coreference Resolution:* For extracting AllenNLP within document coreference
- *AllenNLP Semantic Role Labeling:* For extracting AllenNLP SRL relations 
- *SpaCy Coreference Resolution:* For extracting SpaCy within document coreference
- *WEC-Eng **Cross-Doc** Coreference Resolution (experimental):* For extracting cross-document coreference (more details [here](https://github.com/AlonEirew/cross-doc-event-coref))
- *Stanford Coreference Resolution:* [Can be found in this link](https://github.com/AlonEirew/wd-stanford-coref)

Pre-Requirements
--
- Python 3.6 or higher
- allennlp
- spacy
- Download Within doc SpaCy model from <a href="https://github.com/huggingface/neuralcoref">neuralcoref</a>
- if running ECB+ corpus, download from (<a href="http://www.newsreader-project.eu/results/data/the-ecb-corpus/">Download ECB+</a>)
- download WEC-Eng pre-trained model from [here](https://github.com/AlonEirew/cross-doc-event-coref#wec-eng-pre-trained-model)

Install
--
    pip install -r requirements.txt

Run
--
### Allen Coreference 
`coref_allen.py` Generate within document co-reference using AllenNLP


    python src/coref_allen.py --input_file=ECB+ --output_file=output/allen_wd_coref.json

### Allen SRL
`srl_allen.py` Generate semantic role labeling using AllenNLP


    python src/srl_allen.py --ecb_root_path=ECB+/1 --output_file=output/allen_srl.json

- In order to read the json file back to objects use ``srl_allen.read_srl_json(input_file)`` method

### spaCy Coreference
`coref_spacy.py` Generate within document co-reference using neuralcoref


    python src/coref_spacy.py --input_file=ECB+ --output_file=output/spacy_wd_coref.json --model=en_coref_lg
    
### WEC CD Coreference
`coref_wec_model.py` Generate within document and cross-document coreference using AllenNlp coref and WEC-Eng models.<br/>
This script has been used to generate the entity cross-document coreference facets in [IFacetSum](https://github.com/BIU-NLP/iFACETSUM).<br/>

Using allen coref to predict and cluster within document coreference, then use WEC model to predict and generate cross document clusters.
1) checkout [cross-doc-event-coref](https://github.com/AlonEirew/cross-doc-event-coref) github repository
2) `pip install -e cross-doc-event-coref`
3) Run coref script:
   
    
    python src/coref_wec_model.py --input_file=input/Steroid_Use_docs_formatted.json --output_file=output/Steroid_allen_wd_coref_duc.json --loader=duc --model_file=model/wec_model --cuda=False


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
