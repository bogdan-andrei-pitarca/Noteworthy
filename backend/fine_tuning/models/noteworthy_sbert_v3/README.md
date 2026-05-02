---
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- generated_from_trainer
- dataset_size:1347
- loss:MultipleNegativesRankingLoss
base_model: sentence-transformers/all-mpnet-base-v2
widget:
- source_sentence: fresh citrus and rose petals for spring mornings
  sentences:
  - 'Accords: vanilla, fruity, floral. Notes: green apple, tangerine, almond, cyclamen,
    lotus, orchid, vanilla, tonka bean. Profile: It smells like a fruit stand next
    to an apple orchard, with something sweet and earthy lurking in the background..'
  - 'Accords: green, aromatic, fresh spicy. Notes: mint, grapefruit, bergamot, anise,
    green notes, cassis, rose, hedione. Profile: It smells like citrus peel and bergamot
    at first, then rose petals and white flowers, finishing with a warm, slightly
    powdery base..'
  - 'Accords: coconut, sweet, woody. Notes: coconut, pineapple, lime, apple, bergamot,
    orange, cedar, geranium. Profile: It smells like a fruit stand next to an apple
    orchard — sweet almonds and orange peel mixed with citrus peel, then softened
    by mossy wood..'
- source_sentence: smells like peeling lemons in a warm sunny garden
  sentences:
  - 'Accords: chocolate, warm spicy, citrus. Notes: blood orange, calabrian bergamot,
    dark chocolate, coffee, madagascar vanilla, pancake, maple sap. Profile: It smells
    like sweet orange peel and bergamot at first, then dark chocolate and vanilla,
    with a hint of vanilla sweetness underneath..'
  - 'Accords: animalic, musky. Notes: animal notes, animal notes, animal notes. Profile:
    It smells like a leather jacket left in an animal shelter — soft, earthy, and
    slightly sweet..'
  - 'Accords: floral, citrus, musky. Notes: bergamot, lemon, petitgrain, ginger, nectarine,
    magnolia, freesia, peony. Profile: It smells like citrus peel and lemon at first,
    then soft vanilla and powdery musk, finishing with a warm, slightly bitter sweetness
    that lingers in the air..'
- source_sentence: bright bergamot fading into earthy pepper woods
  sentences:
  - 'Accords: amber, leather, citrus. Notes: lavender, bergamot, amalfi lemon, saffron,
    african orange flower, tonka bean, leather, styrax. Profile: It smells like lavender
    and citrus peel at first, then soft leather and warm saffron, finishing with something
    earthy and slightly powdery..'
  - 'Accords: cherry, amber, warm spicy. Notes: cherry, pepper, incense, agarwood
    (oud), patchouli, moss, benzoin. Profile: It smells like a spice market at dawn
    — sweet cherry and pepper mixed with powdery incense, then settles into something
    earthy and slightly mossy..'
  - 'Accords: citrus, aromatic, woody. Notes: lemon, bergamot, carambola (star fruit),
    cardamom, brazilian rosewood, cedar, tarragon, sage. Profile: It smells like a
    spice market at dawn — citrus peel and cardamom mixed with white flowers, with
    something earthy and slightly woody underneath..'
- source_sentence: fresh minty citrus that dries down warm and earthy
  sentences:
  - 'Accords: white floral, patchouli, floral. Notes: lily of the valley, galbanum,
    ylang ylang, white flowers, jasmine, rose, violet, cassia bourbon. Profile: It
    smells like a flower shop at dawn — white flowers blooming in the background,
    with something powdery and slightly woody underneath..'
  - 'Accords: fresh spicy, aromatic, citrus. Notes: bergamot, pepper, star anise,
    mint, ginger, sage, iris, boxwood. Profile: It smells like bergamot and mint at
    first, then white flowers with a hint of powdery iris, finishing with something
    earthy and slightly woody..'
  - 'Accords: coffee, vanilla, sweet. Notes: lavender, bergamot, cappuccino, raspberry,
    jasmine, virginia cedar, lily-of-the-valley, vanille. Profile: It smells like
    a florist''s coffee shop next to an old church — sweet lavender and white flowers
    mixed with powdery vanilla, finishing with something earthy and slightly woody..'
- source_sentence: bright grapefruit that dries down soft and woody
  sentences:
  - 'Accords: floral, fresh, citrus. Notes: sicilian lemon, lilac, peach blossom,
    green tea, white musk, cedar. Profile: It smells like fresh lemon and lilac at
    first, then soft green tea with a hint of white flowers, finishing with something
    earthy and woody..'
  - 'Accords: chocolate, lactonic, vanilla. Notes: dark chocolate, jasmine, teak wood,
    cedar, chocolate, milk, vanilla, musk. Profile: It smells like dark chocolate
    and white flowers at first, then creamy vanilla and powdery wood, finishing with
    a soft vanilla-musk base..'
  - 'Accords: floral, fruity, citrus. Notes: quince, grapefruit, hyacinth, jasmine,
    musk, iris, virginia cedar, amber. Profile: It smells like citrus peel and hyacinth
    at first, then settles into something earthy and slightly powdery..'
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
      value: 0.9866666793823242
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
    'bright grapefruit that dries down soft and woody',
    'Accords: floral, fruity, citrus. Notes: quince, grapefruit, hyacinth, jasmine, musk, iris, virginia cedar, amber. Profile: It smells like citrus peel and hyacinth at first, then settles into something earthy and slightly powdery..',
    'Accords: floral, fresh, citrus. Notes: sicilian lemon, lilac, peach blossom, green tea, white musk, cedar. Profile: It smells like fresh lemon and lilac at first, then soft green tea with a hint of white flowers, finishing with something earthy and woody..',
]
embeddings = model.encode(sentences)
print(embeddings.shape)
# [3, 768]

# Get the similarity scores for the embeddings
similarities = model.similarity(embeddings, embeddings)
print(similarities)
# tensor([[1.0000, 0.4104, 0.1530],
#         [0.4104, 1.0000, 0.3871],
#         [0.1530, 0.3871, 1.0000]])
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
| **cosine_accuracy** | **0.9867** |

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

* Size: 1,347 training samples
* Columns: <code>sentence_0</code>, <code>sentence_1</code>, and <code>sentence_2</code>
* Approximate statistics based on the first 1000 samples:
  |         | sentence_0                                                                        | sentence_1                                                                         | sentence_2                                                                         |
  |:--------|:----------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|
  | type    | string                                                                            | string                                                                             | string                                                                             |
  | details | <ul><li>min: 8 tokens</li><li>mean: 11.18 tokens</li><li>max: 17 tokens</li></ul> | <ul><li>min: 41 tokens</li><li>mean: 68.59 tokens</li><li>max: 97 tokens</li></ul> | <ul><li>min: 41 tokens</li><li>mean: 68.31 tokens</li><li>max: 91 tokens</li></ul> |
* Samples:
  | sentence_0                                                      | sentence_1                                                                                                                                                                                                                                                                                                        | sentence_2                                                                                                                                                                                                                                                                             |
  |:----------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
  | <code>crisp icy citrus that melts into warm spiced woods</code> | <code>Accords: fresh, aromatic, aquatic. Notes: watery notes, ice, sage, lime, cardamom, artemisia, lavender, bourbon geranium. Profile: It smells like ice cream and lemon peel at first, then warm spices and powdery wood, finishing with something earthy and slightly sweet..</code>                         | <code>Accords: rose, amber, warm spicy. Notes: rose water, black pepper, litchi, olibanum, saffron, rose, agarwood (oud), patchouli. Profile: It smells like a spice market at dawn — sweet rose water mixed with powdery white flowers, then soft leather and warm wood..</code>      |
  | <code>clean aquatic scent with spicy top and cozy base</code>   | <code>Accords: aquatic, fresh, aromatic. Notes: pink pepper, citruses, water notes, geranium, vetiver, amber, patchouli. Profile: It smells like powdery pepper and citrus peel at first, then warm vetiver and amber, with a faint earthy undertone..</code>                                                     | <code>Accords: fruity, marine, white floral. Notes: black currant, melon, dried fruits, red apple, tangerine, lily-of-the-valley, rose, sandalwood. Profile: It smells like dried fruit and melon at first, then rose petals and sandalwood, finishing with a soft woody base..</code> |
  | <code>bergamot tea with dark berries and soft powder</code>     | <code>Accords: citrus, green, fruity. Notes: bergamot, mandarin orange, green tea, black currant, musk, sandalwood, petitgrain, galbanum. Profile: It smells like a spice market at dawn — citrus peel and black currants mixed with white flowers, finishing with something earthy and slightly powdery..</code> | <code>Accords: citrus, aromatic, fresh spicy. Notes: orange, grapefruit, green apple, lavender, thyme, sea notes, patchouli, tonka bean. Profile: It smells like orange peel and citrus peel at first, then thyme and lavender, finishing with a warm, slightly earthy base..</code>   |
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
- `num_train_epochs`: 4
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
- `num_train_epochs`: 4
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
| -1     | -1   | 0.8800                               |
| 1.0    | 43   | 0.9667                               |
| 2.0    | 86   | 0.9733                               |
| 3.0    | 129  | 0.9733                               |
| 3.4884 | 150  | 0.9800                               |
| 4.0    | 172  | 0.9867                               |


### Training Time
- **Training**: 3.0 minutes

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