# Demeter
>In ancient Greek religion and Greek mythology, Demeter is the goddess of the harvest ...

Demeter is meant to be used as a framework for searching for / downloading files of any type in a bulk fashion.  It uses archive.org as well as the Google Custom Search API to download results.  You simply specify the type of file you'd like to download as well as the maximum number of files you'd like to download and Demeter does the rest.

 Demeter verifies file contents by comparing magic numbers to the actual contents of downloaded files.  You can also add new filetypes you'd like to be able to download simply by modifying the 'formats.json' configuration file.  I built this tool with fuzzing in mind, so I will be adding in utilities to aid in fuzzing endeavors.  Currently the only utility provided with the package is the "capsplit" utility, which takes a 'master' libpcap formatted packet capture and splits it into single-packet pcap files.  This was meant to aid fuzzing by providing better code coverage through many small packet captures if you are fuzzing a utility which interacts with pcaps.  More utilities will be added later!

### Usage

```bash
python demeter.py -f exe -m 100
```

This will search archive.org for 100 executable files, if archive.org doesn't have any, it will search google using the Google Custom Search API for up to 100 executable files, then analyze the files to ensure they are valid / save them.  Simple as that!

### Tech

...

### Installation

...

### Plugins

...

### Development

...

### Todos

- Finish coding
- Finish this readme!