### Release 2.1
Released 07.02.2021

* Fixed bugs with Python v3.9

### Release 2.0
Released 22.06.2019

* Added new corpora
  * [Adyghe corpus](http://web-corpora.net/AdygheCorpus/search/)
  * [Albanian corpus](http://web-corpora.net/AlbanianCorpus/search/)
  * [Eastern Armenian corpus](http://eanc.net)
  * [Buryat corpus](http://web-corpora.net/BuryatCorpus/search/)
  * [Danish corpus](https://ordnet.dk/korpusdk_en/concordance)
  * [German corpus](https://www.dwds.de)
  * [Estonian corpus](http://www.cl.ut.ee/korpused/kasutajaliides/index.php)
  * [Modern Greek corpus](http://web-corpora.net/GreekCorpus/search/)
  * [Hindi corpus](http://www.cfilt.iitb.ac.in/~corpus/hindi/find.php)
  * [Kalmyk corpus](http://web-corpora.net/KalmykCorpus/search/)
  * [Georgian monolingual corpus](http://corpora.iliauni.edu.ge)
  * [Almaty corpus of the Kazakh language](http://web-corpora.net/KazakhCorpus/search/)
  * [Mongolian corpus](http://web-corpora.net/MongolianCorpus/search/)
  * [Polish-Russian Parallel Corpus](http://pol-ros.polon.uw.edu.pl/)
  * [Tatar corpus](http://web-corpora.net/TatarCorpus/)
  * [Udmurt corpus](http://web-corpora.net/UdmurtCorpus/search/)
  * [Modern Yiddish corpus](http://web-corpora.net/YNC/search/)
  * [Chinese-English subcorpus of JuKuu corpus](http://www.jukuu.com/)
* Renamed several search parameters
  * `numResults` -> `n_results`
  * `nLeft` -> `n_left`
  * `nRight` -> `n_right`
  * `queryLanguage` -> `query_language`
  * `tag` -> `analysis`
  * `writingSystem` -> `writing_system`
* Added search parameter `gr_tags` (for Russian National Corpus only)
* Renamed `Target` attribute `tags` -> `analysis` and added attribute `gr_tags`
* `Target.analysis` always returned as `list`

 
### Release 1.1
Released 01.04.2018

* 5 corpora, including a parallel one
* `Corpus` object for searching, storing results and retrying failed queries
* `Result` object for storing all results and export to `csv`
* `Target` object for managing occurrences 
