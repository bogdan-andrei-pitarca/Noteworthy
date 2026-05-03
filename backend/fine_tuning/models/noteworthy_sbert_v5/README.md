---
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- generated_from_trainer
- dataset_size:1341
- loss:MultipleNegativesRankingLoss
base_model: sentence-transformers/all-mpnet-base-v2
widget:
- source_sentence: fruity sweet fragrance raspberry caramel
  sentences:
  - 'Accords: powdery, amber, vanilla. Notes: plum, chinese cinnamon wood, iris, violet,
    lily, anise, jasmine, mimosa. Profile: It smells like a flower shop at dawn —
    sweet plums and white flowers mixed with powdery flowers, then settles into something
    earthy and resinous..'
  - 'Accords: sweet, caramel, vanilla. Notes: raspberry, orange, bergamot, fig leaf,
    cotton candy, licorice, strawberry, red berries. Profile: It smells like ripe
    raspberries and orange peel at first, then sweet vanilla and caramel, finishing
    with a soft vanilla-musk base..'
  - 'Accords: sweet, rose, vanilla. Notes: cinnamon, pink pepper, bulgarian rose,
    madagascar vanilla, toffee, amber, musk. Profile: It smells like a spice cabinet
    left open in an old wood stove, with something sweet and earthy lurking in the
    background..'
- source_sentence: warm pink pepper and cedar fragrance
  sentences:
  - 'Accords: cinnamon, warm spicy, amber. Notes: mandarin orange, patchouli, bergamot,
    cinnamon, amber, virginia cedar, leather, musk. Profile: It smells like orange
    peel and citrus peel at first, then warm leather and soft wood, finishing with
    a hint of earthy wood..'
  - 'Accords: mossy, woody, fruity. Notes: black currant, caraway, coriander, jasmine,
    lily-of-the-valley, oakmoss, sandalwood, musk. Profile: It smells like sweet black
    currants and caraway at first, then white flowers and moss, finishing with something
    earthy and slightly woody..'
  - 'Accords: cinnamon, warm spicy, musky. Notes: apple, violet leaf, bergamot, cinnamon,
    pink pepper, geranium, musk, cedar. Profile: It smells like ripe apples and citrus
    peel at first, then warm spices and powdery cedar, finishing with a soft woody
    base..'
- source_sentence: sweet creamy vanilla with citrus
  sentences:
  - 'Accords: vanilla, yellow floral, green. Notes: black currant, bergamot, narcissus,
    gardenia, vanila, tonka bean. Profile: It smells like sweet black currants and
    bergamot at first, then soft narcissus and vanilla, finishing with a warm, earthy
    base..'
  - 'Accords: honey, sweet, fruity. Notes: pear, jasmine, honey. Profile: It smells
    like fresh pear and jasmine at first, then sweet honey and warm honey..'
  - 'Accords: vanilla, sweet, warm spicy. Notes: saffron, thyme, mandarin orange,
    lily, ylang-ylang, orchid, vanilla, tonka bean. Profile: It smells like citrus
    peel and thyme at first, then creamy vanilla and sweet vanilla, with a hint of
    powdery wood underneath..'
- source_sentence: spicy ginger cologne for men
  sentences:
  - 'Accords: warm spicy, woody, fresh spicy. Notes: bergamot, citron, cardamom, lavender,
    nutmeg, clove, rosemary, pink pepper. Profile: It smells like a spice market at
    dawn — citrus peel and cardamom mixed with powdery spices, then softens into something
    earthy and slightly sweet..'
  - 'Accords: warm spicy, citrus, aromatic. Notes: ginger, bergamot, lemon, spices,
    violet leaf, white pepper, basil, tonka bean. Profile: It smells like a spice
    market at dawn — citrus peel mixed with powdery white flowers, then softens into
    something earthy and slightly sweet..'
  - 'Accords: herbal, leather, aromatic. Notes: artemisia, incense, lemon, leather,
    chamomile, apricot, iris, vanilla. Profile: It smells like a leather jacket left
    open in an old church — dried herbs mixed with white flowers, then softens into
    something powdery and slightly woody..'
- source_sentence: clean soapy smell with orange blossom
  sentences:
  - 'Accords: lavender, aromatic, iris. Notes: pink pepper, rhubarb, pink grapefruit,
    lavender, orris, tuberose, freesia, tonka bean. Profile: It smells like a spice
    market at dawn — sweet pepper and citrus peel mixed with white flowers, then soft
    wood and something earthy and slightly powdery..'
  - 'Accords: amber, balsamic, sweet. Notes: mandarin orange, bergamot, lily-of-the-valley,
    myrhh, jasmine, opoponax, amber, patchouli. Profile: It smells like citrus peel
    and bergamot at first, then white flowers with a hint of powdery amber, finishing
    with something sweet and slightly floral..'
  - 'Accords: lavender, woody, musky. Notes: lavender, pink pepper, neroli, aldehydes,
    orris, petalia, blackberry leaf, orange blossom. Profile: It smells like powdery
    lavender and citrus peel at first, then soft woods and musk, with a warm, slightly
    woody base..'
pipeline_tag: sentence-similarity
library_name: sentence-transformers
metrics:
- cosine_accuracy
model-index:
- name: SentenceTransformer based on sentence-transformers/all-mpnet-base-v2
  results:
  - task:
      type: triplet
      name: Triplet
    dataset:
      name: fragrance triplet v3
      type: fragrance-triplet-v3
    metrics:
    - type: cosine_accuracy
      value: 0.8733333349227905
      name: Cosine Accuracy
---

# SentenceTransformer based on sentence-transformers/all-mpnet-base-v2

This is a [sentence-transformers](https://www.SBERT.net) model finetuned from [sentence-transformers/all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2). It maps sentences & paragraphs to a 768-dimensional dense vector space and can be used for retrieval.

## Model Details

### Model Description
- **Model Type:** Sentence Transformer
- **Base model:** [sentence-transformers/all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2) <!-- at revision e8c3b32edf5434bc2275fc9bab85f82640a19130 -->
- **Maximum Sequence Length:** 384 tokens
- **Output Dimensionality:** 768 dimensions
- **Similarity Function:** Cosine Similarity
- **Supported Modality:** Text
<!-- - **Training Dataset:** Unknown -->
<!-- - **Language:** Unknown -->
<!-- - **License:** Unknown -->

### Model Sources

- **Documentation:** [Sentence Transformers Documentation](https://sbert.net)
- **Repository:** [Sentence Transformers on GitHub](https://github.com/huggingface/sentence-transformers)
- **Hugging Face:** [Sentence Transformers on Hugging Face](https://huggingface.co/models?library=sentence-transformers)

### Full Model Architecture

```
SentenceTransformer(
  (0): Transformer({'transformer_task': 'feature-extraction', 'modality_config': {'text': {'method': 'forward', 'method_output_name': 'last_hidden_state'}}, 'module_output_name': 'token_embeddings', 'architecture': 'MPNetModel'})
  (1): Pooling({'embedding_dimension': 768, 'pooling_mode': 'mean', 'include_prompt': True})
  (2): Normalize({})
)
```

## Usage

### Direct Usage (Sentence Transformers)

First install the Sentence Transformers library:

```bash
pip install -U sentence-transformers
```
Then you can load this model and run inference.
```python
from sentence_transformers import SentenceTransformer

# Download from the 🤗 Hub
model = SentenceTransformer("sentence_transformers_model_id")
# Run inference
sentences = [
    'clean soapy smell with orange blossom',
    'Accords: lavender, woody, musky. Notes: lavender, pink pepper, neroli, aldehydes, orris, petalia, blackberry leaf, orange blossom. Profile: It smells like powdery lavender and citrus peel at first, then soft woods and musk, with a warm, slightly woody base..',
    'Accords: lavender, aromatic, iris. Notes: pink pepper, rhubarb, pink grapefruit, lavender, orris, tuberose, freesia, tonka bean. Profile: It smells like a spice market at dawn — sweet pepper and citrus peel mixed with white flowers, then soft wood and something earthy and slightly powdery..',
]
embeddings = model.encode(sentences)
print(embeddings.shape)
# [3, 768]

# Get the similarity scores for the embeddings
similarities = model.similarity(embeddings, embeddings)
print(similarities)
# tensor([[1.0000, 0.3105, 0.2230],
#         [0.3105, 1.0000, 0.7162],
#         [0.2230, 0.7162, 1.0000]])
```
<!--
### Direct Usage (Transformers)

<details><summary>Click to see the direct usage in Transformers</summary>

</details>
-->

<!--
### Downstream Usage (Sentence Transformers)

You can finetune this model on your own dataset.

<details><summary>Click to expand</summary>

</details>
-->

<!--
### Out-of-Scope Use

*List how the model may foreseeably be misused and address what users ought not to do with the model.*
-->

## Evaluation

### Metrics

#### Triplet

* Dataset: `fragrance-triplet-v3`
* Evaluated with [<code>TripletEvaluator</code>](https://sbert.net/docs/package_reference/sentence_transformer/evaluation.html#sentence_transformers.sentence_transformer.evaluation.TripletEvaluator)

| Metric              | Value      |
|:--------------------|:-----------|
| **cosine_accuracy** | **0.8733** |

<!--
## Bias, Risks and Limitations

*What are the known or foreseeable issues stemming from this model? You could also flag here known failure cases or weaknesses of the model.*
-->

<!--
### Recommendations

*What are recommendations with respect to the foreseeable issues? For example, filtering explicit content.*
-->

## Training Details

### Training Dataset

#### Unnamed Dataset

* Size: 1,341 training samples
* Columns: <code>sentence_0</code>, <code>sentence_1</code>, and <code>sentence_2</code>
* Approximate statistics based on the first 1000 samples:
  |         | sentence_0                                                                       | sentence_1                                                                         | sentence_2                                                                        |
  |:--------|:---------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|
  | type    | string                                                                           | string                                                                             | string                                                                            |
  | details | <ul><li>min: 5 tokens</li><li>mean: 8.32 tokens</li><li>max: 13 tokens</li></ul> | <ul><li>min: 40 tokens</li><li>mean: 68.86 tokens</li><li>max: 89 tokens</li></ul> | <ul><li>min: 42 tokens</li><li>mean: 67.1 tokens</li><li>max: 91 tokens</li></ul> |
* Samples:
  | sentence_0                                               | sentence_1                                                                                                                                                                                                                                                                                                                                               | sentence_2                                                                                                                                                                                                                                                                                           |
  |:---------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
  | <code>warm cozy café smell with cinnamon</code>          | <code>Accords: sweet, white floral, warm spicy. Notes: almond, coffee, bergamot, lemon, tuberose, jasmine sambac, orange blossom, orris. Profile: It smells like sweet almonds and coffee at first, then creamy vanilla and powdery roses, finishing with a soft woody base..</code>                                                                     | <code>Accords: sweet, coconut, amber. Notes: ylang-ylang, pepper, bergamot, coconut, salt, orchid, jasmine sambac, tonka bean. Profile: It smells like a spice market at dawn — sweet pepper and spice mixed with powdery sandalwood, then settles into something earthy and slightly woody..</code> |
  | <code>fresh floral spicy rose scent</code>               | <code>Accords: rose, floral, fresh. Notes: cassia, lemon verbena, star anise, rose, peony, magnolia, taif rose, musk. Profile: It smells like a flower shop at dawn — sweet citrus and roses mixed with powdery flowers, then soft vanilla and musk..</code>                                                                                             | <code>Accords: rose, musky, powdery. Notes: orange, pink pepper, turkey red rose, iris, musk, cedar. Profile: It smells like orange peel and spice at first, then iris and resin, with a soft, slightly woody base..</code>                                                                          |
  | <code>tropical fruit perfume with oud and leather</code> | <code>Accords: oud, fruity, leather. Notes: passionfruit, fruity notes, turkish rose, saffron, agarwood (oud), indonesian patchouli leaf, benzoin, leather. Profile: It smells like a leather jacket left in an old wooden workshop — citrus peel and saffron mixed with resinous wood, then softens into something earthy and slightly powdery..</code> | <code>Accords: oud, musky, fruity. Notes: raspberry, bergamot, agarwood (oud), ambroxan, musk. Profile: It smells like ripe raspberries and bergamot at first, then settles into something earthy and slightly woody..</code>                                                                        |
* Loss: [<code>MultipleNegativesRankingLoss</code>](https://sbert.net/docs/package_reference/sentence_transformer/losses.html#multiplenegativesrankingloss) with these parameters:
  ```json
  {
      "scale": 20.0,
      "similarity_fct": "cos_sim",
      "gather_across_devices": false,
      "directions": [
          "query_to_doc"
      ],
      "partition_mode": "joint",
      "hardness_mode": null,
      "hardness_strength": 0.0
  }
  ```

### Training Hyperparameters
#### Non-Default Hyperparameters

- `per_device_train_batch_size`: 32
- `per_device_eval_batch_size`: 32
- `multi_dataset_batch_sampler`: round_robin

#### All Hyperparameters
<details><summary>Click to expand</summary>

- `do_predict`: False
- `prediction_loss_only`: True
- `per_device_train_batch_size`: 32
- `per_device_eval_batch_size`: 32
- `gradient_accumulation_steps`: 1
- `eval_accumulation_steps`: None
- `torch_empty_cache_steps`: None
- `learning_rate`: 5e-05
- `weight_decay`: 0.0
- `adam_beta1`: 0.9
- `adam_beta2`: 0.999
- `adam_epsilon`: 1e-08
- `max_grad_norm`: 1
- `num_train_epochs`: 3
- `max_steps`: -1
- `lr_scheduler_type`: linear
- `lr_scheduler_kwargs`: None
- `warmup_ratio`: None
- `warmup_steps`: 0
- `log_level`: passive
- `log_level_replica`: warning
- `log_on_each_node`: True
- `logging_nan_inf_filter`: True
- `enable_jit_checkpoint`: False
- `save_on_each_node`: False
- `save_only_model`: False
- `restore_callback_states_from_checkpoint`: False
- `use_cpu`: False
- `seed`: 42
- `data_seed`: None
- `bf16`: False
- `fp16`: False
- `bf16_full_eval`: False
- `fp16_full_eval`: False
- `tf32`: None
- `local_rank`: -1
- `ddp_backend`: None
- `debug`: []
- `dataloader_drop_last`: False
- `dataloader_num_workers`: 0
- `dataloader_prefetch_factor`: None
- `disable_tqdm`: False
- `remove_unused_columns`: True
- `label_names`: None
- `load_best_model_at_end`: False
- `ignore_data_skip`: False
- `fsdp`: []
- `fsdp_config`: {'min_num_params': 0, 'xla': False, 'xla_fsdp_v2': False, 'xla_fsdp_grad_ckpt': False}
- `accelerator_config`: {'split_batches': False, 'dispatch_batches': None, 'even_batches': True, 'use_seedable_sampler': True, 'non_blocking': False, 'gradient_accumulation_kwargs': None}
- `parallelism_config`: None
- `deepspeed`: None
- `label_smoothing_factor`: 0.0
- `optim`: adamw_torch_fused
- `optim_args`: None
- `group_by_length`: False
- `length_column_name`: length
- `project`: huggingface
- `trackio_space_id`: trackio
- `ddp_find_unused_parameters`: None
- `ddp_bucket_cap_mb`: None
- `ddp_broadcast_buffers`: False
- `dataloader_pin_memory`: True
- `dataloader_persistent_workers`: False
- `skip_memory_metrics`: True
- `push_to_hub`: False
- `resume_from_checkpoint`: None
- `hub_model_id`: None
- `hub_strategy`: every_save
- `hub_private_repo`: None
- `hub_always_push`: False
- `hub_revision`: None
- `gradient_checkpointing`: False
- `gradient_checkpointing_kwargs`: None
- `include_for_metrics`: []
- `eval_do_concat_batches`: True
- `auto_find_batch_size`: False
- `full_determinism`: False
- `ddp_timeout`: 1800
- `torch_compile`: False
- `torch_compile_backend`: None
- `torch_compile_mode`: None
- `include_num_input_tokens_seen`: no
- `neftune_noise_alpha`: None
- `optim_target_modules`: None
- `batch_eval_metrics`: False
- `eval_on_start`: False
- `use_liger_kernel`: False
- `liger_kernel_config`: None
- `eval_use_gather_object`: False
- `average_tokens_across_devices`: True
- `use_cache`: False
- `prompts`: None
- `batch_sampler`: batch_sampler
- `multi_dataset_batch_sampler`: round_robin
- `router_mapping`: {}
- `learning_rate_mapping`: {}

</details>

### Training Logs
| Epoch  | Step | fragrance-triplet-v3_cosine_accuracy |
|:------:|:----:|:------------------------------------:|
| -1     | -1   | 0.7667                               |
| 1.0    | 42   | 0.8533                               |
| 1.1905 | 50   | 0.8733                               |


### Training Time
- **Training**: 1.1 minutes

### Framework Versions
- Python: 3.12.13
- Sentence Transformers: 5.4.1
- Transformers: 5.0.0
- PyTorch: 2.10.0+cu128
- Accelerate: 1.13.0
- Datasets: 4.0.0
- Tokenizers: 0.22.2

## Citation

### BibTeX

#### Sentence Transformers
```bibtex
@inproceedings{reimers-2019-sentence-bert,
    title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
    author = "Reimers, Nils and Gurevych, Iryna",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",
    month = "11",
    year = "2019",
    publisher = "Association for Computational Linguistics",
    url = "https://arxiv.org/abs/1908.10084",
}
```

#### MultipleNegativesRankingLoss
```bibtex
@misc{oord2019representationlearningcontrastivepredictive,
      title={Representation Learning with Contrastive Predictive Coding},
      author={Aaron van den Oord and Yazhe Li and Oriol Vinyals},
      year={2019},
      eprint={1807.03748},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/1807.03748},
}
```

<!--
## Glossary

*Clearly define terms in order to be accessible across audiences.*
-->

<!--
## Model Card Authors

*Lists the people who create the model card, providing recognition and accountability for the detailed work that goes into its construction.*
-->

<!--
## Model Card Contact

*Provides a way for people who have updates to the Model Card, suggestions, or questions, to contact the Model Card authors.*
-->