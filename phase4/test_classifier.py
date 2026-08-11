import torch
from text_classifier import TextClassifier, tokenize, clean_text

def test_clean_text_fixes_html_entity():
    result = clean_text("Web #39;s No. 1")
    assert "#39;" not in result
    assert "'s" in result  # confirms the apostrophe was correctly substituted

def test_tokenize_lowercases():
    tokens = tokenize("Wall Street's")
    assert "wall" in tokens
    assert "Wall" not in tokens

def test_model_output_shape():
    model = TextClassifier(vocab_size=1000, embed_dim=32, num_classes=4)
    sample_input = torch.randint(0, 1000, (5, 30))  # 5 examples, 30 tokens each
    output = model(sample_input)
    assert output.shape == (5, 4)