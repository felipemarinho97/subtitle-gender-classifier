# Subtitle gender classifier 
- This repo contains the inference code to use pretrained human voice gender classifier.
- It also contains the code to tag subtitles files.
- This is a fork of the [voice-gender-classifier](https://github.com/JaesungHuh/voice-gender-classifier.git)

## Installation
First, clone this repository
```
git clone https://github.com/felipemarinho97/subtitle-gender-classifier.git
```

and install the packages via pip.

```
cd subtitle-gender-classifier
pip install -r requirements.txt
```

## Usage
To detect the gender of the speaker in some audio file, run the following command:

```
python detect.py <path_to_audio_file>
```

To tag a subtitle file with gender metadata, run the following command:

```
python gender_tagging.py input_subtitles.srt input_video.mp4 output_subtitles.srt
```

The output subtitle file will gender metadata like this:
```
1
00:01:15,040 --> 00:01:17,519
<female>Miss Tracy, have a smile</female>

2
00:01:19,240 --> 00:01:20,879
<female>Please look this way</female>

3
00:01:23,480 --> 00:01:24,999
<male>Tracy, cheers</male>

4
00:01:25,080 --> 00:01:25,919
<male>Great</male>
```

## Pretrained weights
For those who need pretrained weights, please download them in [here](https://drive.google.com/file/d/1ojtaa6VyUhEM49F7uEyvsLSVN3T8bbPI/view?usp=sharing)

## Training details
State-of-the-art speaker verification model already produces good representation of the speaker's gender.

I used the pretrained ECAPA-TDNN from [TaoRuijie's](https://github.com/TaoRuijie/ECAPA-TDNN) repository, added one linear layer to make two-class classifier, and finetuned the model with the VoxCeleb2 dev set.

The model achieved **98.7%** accuracy on the VoxCeleb1 identification test split.

## Caveat
I would like to note the training dataset I've used for this model (VoxCeleb) may not represent the global human population. Please be careful of unintended biases when using this model.

## Reference
- 🤗 [Huggingface Hub link](https://huggingface.co/JaesungHuh/ecapa-gender)
- I modified the model architecture from [TaoRuijie's](https://github.com/TaoRuijie/ECAPA-TDNN) repository.
- For more details about ECAPA-TDNN, check the [paper](https://arxiv.org/abs/2005.07143).