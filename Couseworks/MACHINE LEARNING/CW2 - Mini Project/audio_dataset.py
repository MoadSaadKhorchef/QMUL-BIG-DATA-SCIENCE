import os
import random
import numpy as np
import pandas as pd
import torchaudio


def extract_col(df, col_name):
    """Extract a column define by col_name from the input dataframe.

    Parameters
    ----------
    df : (mandatory)
        the input dataframe.
    col_name : str (mandatory)
        contrain the name of the column to be extracted.

    Returns
    -------
    numpy.array:
        contain the values present in the extracted column.
    """
    return df[col_name].to_numpy()


def get_path(df, file_col_name, folder="wav", base_path=None):
    """Return a list contain the full path of each row in the a specific column.

    Parameters
    ----------
    df: (mandatory)
        the input dataframe.
    file_col_name: str (mandatory)
        the name of the column contain the file names.
    base_path: str, default None
        the path to the excel file.

    Returns
    -------
    paths: numpy.array
        contain the full path for each data in the excel file.
    """
    files = extract_col(df=df, col_name=file_col_name)
    paths = []
    for i in range(len(files)):
        paths.append(os.path.join(base_path, folder, files[i]))
    return paths


class Audio(Dataset):
    def __init__(self, config_file_path, labels_GT, is_num_classification, resample_freq):
        self.labels_GT = labels_GT
        self.resample_freq = resample_freq

        data_root_path = os.path.dirname(config_file_path)
        df = pd.read_excel(config_file_path)

        self.paths = get_path(df=df, base_path=data_root_path,
                              folder="wav", file_col_name="File")

        if is_num_classification:
            self.classes = self.to_int_label(df=df, col_name="Label_GT")
        else:
            self.classes = self.to_int_label(df=df, col_name="")

    def __len__(self):
        return len(self.paths)

    def to_int_label(self, df, col_name):
        """Transform the label to an ordinal class number.

        For optimization purposes this methode count the recurrence for each
        label.

        Parameters
        ----------
        df: (mandatory)
            the input dataframe.
        col_name: str (mandatory)
            contain the name of the column to be converted.

        Returns
        -------
        records: numpy.array
            contrain the class number for each target.
        """
        records = np.zeros(len(df[col_name]), dtype=float)
        for i in range(len(df[col_name])):
            records[i] = self.labels_GT[df[col_name][i]]
            #self.count[int(records[i])] += 1

        return records

    def __getitem__(self, i):

        soundData, sample_rate = torchaudio.load(path[i], out = None,
                                             normalization = True)

        resample_transform = torchaudio.transforms.Resample(
            orig_freq=sample_rate, new_freq=self.resample_freq)

        soundData = resample_transform(soundData)

        # This will convert audio files with two channels into one
        soundData = torch.mean(soundData, dim=0, keepdim=True)

        # Convert audio to log-scale Mel spectrogram
        melspectrogram_transform = torchaudio.transforms.MelSpectrogram(
            sample_rate=self.resample, n_mels=self.n_mels)
        melspectrogram = melspectrogram_transform(soundData)
        melspectogram_db = torchaudio.transforms.AmplitudeToDB()(melspectrogram)

        #Make sure all spectrograms are the same size
        fixed_length = 3 * (self.resample_freq//200)
        if melspectogram_db.shape[2] < fixed_length:
            melspectogram_db = torch.nn.functional.pad(
                melspectogram_db, (0, fixed_length - melspectogram_db.shape[2]))
        else:
            melspectogram_db = melspectogram_db[:, :, :fixed_length]

        target = self.classes[i]

        return melspectogram_db, self.classes[i]
