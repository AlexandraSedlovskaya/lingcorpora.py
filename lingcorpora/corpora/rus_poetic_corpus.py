from ..params_container import Container
from ..target import Target

from bs4.element import Comment, Tag
import re
import requests
from bs4 import BeautifulSoup
import time
from urllib import parse
from random import randint

__doc__ = \
    """
National Corpus of Russian: Poetic subcorpus

API for Poetic subcorpus (https://ruscorpora.ru/new/search-poetic.html)

Search Parameters:
query: str or list([str])
    query or queries (currently only exact search by word or phrase is available)
num_results: int, default 100
    number of results wanted
get_analysis: bool, default False
    whether to collect grammatical tags for target word or not 
    or whether to collect text anlysis if query empty
stress: bool, default False
    whether to collect texts with stress or not
markup: bool, default False
    whether to collect texts with line markup or not
exact: bool, default True
    enable exact search or lexeme search
subcorpus: dict, default None
    subcorpus parameters:
        ['doc_genre_fi', 'doc_language', 'doc_meter', 'doc_feet', 'doc_clausula',
         'doc_strophe', 'doc_strophe_gr', 'doc_rhyme', 'doc_extra', 's_sp_frm_sch']
         
Example

.. code-block:: python

    corp = lingcorpora.Corpus('rus_poetic')
    results = corp.search('путь', exact=False, stress=True,
                          subcorpus={'doc_genre_fi': ['стихотворение'], 'doc_language': ['английский']}, n_results=10)
    for result in results:
        for i, target in enumerate(result):
            print(i+1, target.text)
            
.. parsed-literal::

    "путь": 100%|██████████| 10/10 [00:01<00:00,  6.22docs/s]
    1 Зака̀нчива̀я пу̀ть земно̀й, Всем сплѐтника̀м напо̀мню я̀: Так ѝли ѝначѐ, со мно̀й Ещѐ вы встрѐтитѐсь друзья̀!
    2 Можно смѐло повѐрить сия̀нью― Вслед за нѝм мы напра̀вим наш пу̀ть: Можно смѐло повѐрить сия̀нью― Нас не мо̀жет оно̀ обману̀ть!»
    3 Так прошлѝ до конца̀ мы аллѐю И могѝла закры̀ла нам пу̀ть, К склепу с на̀дписью вы̀вел нас пу̀ть.
    4 Так прошлѝ до конца̀ мы аллѐю И могѝла закры̀ла нам пу̀ть, К склепу с на̀дписью вы̀вел нас пу̀ть.
    5 Бы̀стро, гру̀бо ѝ умѐло за̀ коро̀ткий пу̀ть земно̀й Ѝ мой ду̀х, и мо̀е тѐло вы̀муштро̀вала̀ война̀.
    6 Стоѝт стару̀ха на̀ путѝ, Вся смо̀рщила̀сь от слѐз.
    7 3. КАРЕТА Катѝ, катѝ, карѐта, По то̀рному̀ путѝ! Ах, на̀до б до̀ рассвѐта Наслѐдство о̀брестѝ!..
    8 За зо̀лото̀м в пого̀ню― По то̀рному̀ путѝ!
    9 Спешу̀ я, у̀томя̀сь, к целѝтельно̀й постѐли, где пло̀ти су̀ждено̀ от стра̀нствий о̀тдохну̀ть, ― но то̀лько всѐ труды̀ от тѐла о̀тлетѐли, пуска̀ется̀ мой у̀м в пало̀мничѐский пу̀ть.
    10 Следѝл я, ка̀к луна̀ во мра̀ке сверша̀ла кра̀дучѝсь свой пу̀ть― по стѐнке, в зѐркалѐ, на ча̀шке … Я в э̀ту но̀чь не мо̀г усну̀ть.
    
    .. code-block:: python
    
    results = corp.search('', subcorpus={'s_sp_frm_sch': ['Дк4ж 1*1*4*1']}, n_results=5, get_analysis=True)
    for result in results:
        for i, target in enumerate(result):
            print(i+1, target.text)
            print(target.analysis)
            
    .. parsed-literal::
    
    "": 100%|██████████| 5/5 [00:20<00:00,  4.06s/docs]
    1 Маршак угощал меня чаем с печеньем, Чуковский книгами и беседой, Слуцкий супом, Мартынов камнями, Тарковский грузинским вином и сыром, Глазков армянским коньяком и« Записками великого гуманиста», Домбровский пивом с прицепом, скорописью школьных тетрадок в линейку и селем экстатического клокотанья, Шаламов содержимым своего сундучка, где были валенки, рукавицы, кожух, ушанка― все, что нужно, когда придут оттуда и дадут пять минут на сборы, а под шмотьем― машинопись в трех томах, переплетенных вручную, плюс однотомник, тоже машинопись, но в ледерине― подарок из новосибирского Академгородка― сколько их, старших друзей и спутников, обогревавших меня, согревших своим вниманием и поддержкой, список можно бы длить и длить, он долог, хотя, возможно, короче живописной росписи предков Кузмина и тьмы театральных почитателей Гумилева, но он и не мал, потому что Бог одарил меня почтенным возрастом, а по меркам века девятнадцатого― долголетием, хотя солидностью и степенностью не обременил, по счастью, ― так вот, я мог бы утроить свои богатства, изукрасить подробностями их и прочим, но я не люблю ничего сугубого, а они становятся вроде приема, как современная архитектура наружу цветными коммуникациями вроде парижского Центра Помпиду … Что я хочу сказать? не знаю. Я только думаю: ну а сам- то, кого приветил я сам и чем?…
    {'Автор': 'О. Г. Чухонцев', 'Пол автора': 'муж', 'Дата рождения автора': '1938', 'Название': '«Маршак угощал меня чаем с печеньем...»', 'Дата создания': '2016', 'Точность даты': 'неточная', 'Книга стихов': 'Выходящее из уходящее за (2016)', 'Жанр': 'стихотворение', 'Число строк': '39', 'Строфика': '0', 'Метр': 'Ан, Аф, Д, тонический : Тк', 'Число стоп/иктов/слогов': 'вольная : 3,4,5,6', 'Клаузула': 'вольная : г, д, ж, м', 'Рифма': '0', 'Дополнительные параметры': 'переменная анакруса', 'Метрическая формула': 'Тк3,4,5,6г,д,ж,м', 'Предложений': '4', 'Словоформ': '193'}
    2 4. ЕЩЕ ЭПИТАФИЯ … куда ж нам плыть? Волна горька, И у нее глаза хорька― Сужающиеся блики, И шум от нее великий. Куда лететь? Свод недвижим― То облако, то недожим Воздутой воздушной ткани, И на горах бьют молотками. Куда идти? В лесу война, В реке шуршащая волна, А в небе страшные стуки И разные другие штуки. Бьют молотками на горах, Огни шарахаются― шарах! А мы лежим, как смерть золотая, Не уплывая, не улетая …
    {'Автор': 'О. А. Юрьев', 'Пол автора': 'муж', 'Дата рождения автора': '1959', 'Название': 'Еще эпитафия : «…куда ж нам плыть? Волна горька...»', 'Дата создания': '2013-2014', 'Цикл': 'Эпиграммы и эпитафии, 4', 'Жанр': 'стихотворение : цикл : эпитафия', 'Число строк': '16', 'Строфика': '2', 'Метр': 'Я, тонический : Дк', 'Число стоп/иктов/слогов': 'вольная : 3,4', 'Клаузула': 'регулярная : ммжж', 'Рифма': 'парная : аа', 'Метрическая формула': 'Дк3,4ммжж', 'Предложений': '9', 'Словоформ': '72'}
    3 ХОЛМЫ. УХОД где вы где мы сквозь пар не вижу я кровяный― одни сизо- синие холмы их зачехленные караваны зачем? куда? и здесь быть небу синю и сизу и здесь фыркнет звездная вода и двинется сквозь землю снизу мы с- подо льда напьемся гибельной и звездной воды― и станем как звезда и вы бы с нами … ― но поздно, поздно: еще до тьмы они шатры свои скатали и в небо тронулись― с детьми и домочадцами и скотами VIII, 12
    {'Автор': 'О. А. Юрьев', 'Пол автора': 'муж', 'Дата рождения автора': '1959', 'Название': 'Холмы. Уход : «где вы где мы…»', 'Дата создания': '2012', 'Книга стихов': 'О Родине (2013)', 'Жанр': 'стихотворение', 'Число строк': '16', 'Строфика': '4', 'Метр': 'Я, тонический : Дк', 'Число стоп/иктов/слогов': '4(2)', 'Клаузула': 'регулярная : мж', 'Рифма': 'перекрестная : абаб', 'Метрическая формула': 'Дк4мж; Дк2м', 'Предложений': '9', 'Словоформ': '78'}
    4 Внизу, у дороги К машине, едущей с горы( хворост небесный растворя) во мглы сияние дождевое, зачем приделаны шары из выщелоченного хрусталя со смятой сеточкой в обвое? Зачем искрится головой( раствор надземный раздвоя на пресное и дрожжевое) дождик дорожный угловой из вышелушенного хрусталя? … или же нет, и их тоже двое?
    {'Автор': 'О. А. Юрьев', 'Пол автора': 'муж', 'Дата рождения автора': '1959', 'Название': 'Внизу, у дороги : «К машине, едущей с горы...»', 'Дата создания': '2007-2010', 'Книга стихов': 'Стихи и другие стихотворения (2011)', 'Жанр': 'стихотворение', 'Число строк': '12', 'Строфика': '0', 'Метр': 'Я, тонический : Дк', 'Число стоп/иктов/слогов': 'вольная : 4(5)', 'Клаузула': 'вольная : ж, м', 'Рифма': 'вольная', 'Дополнительные параметры': 'перебои', 'Метрическая формула': 'Я4ж,м; Дк4ж, Я5м', 'Предложений': '4', 'Словоформ': '49'}
    5 Гимн О клене клеёном, О склоне слоеном, О дождике сонном, что летя пересох, О свете каленом, О лете соленом, О белой воде, что летит, как песок, О рое, парящем над райским районом, О небе, снижающемся наискосок Ласточки кричат на выдохе И срываются над рекой: Раскрываются на выходе И скрываются под рукой; А река― вся дым зеркальный, Над ней заря― вся зеркала, Из них змеею пирамидальной Тьма выезжает, как юла … На вдохе ласточка молчит, На вдохе дождик не стучит, И темнота над раем, И мы не умираем.
    {'Автор': 'О. А. Юрьев', 'Пол автора': 'муж', 'Дата рождения автора': '1959', 'Название': 'Гимн : «О клене клеёном...»', 'Дата создания': '2007-2010', 'Книга стихов': 'Стихи и другие стихотворения (2011)', 'Жанр': 'стихотворение', 'Число строк': '20', 'Строфика': '0', 'Метр': 'Аф, Х, Я, тонический : Дк', 'Число стоп/иктов/слогов': 'вольная : 3,4(2)', 'Клаузула': 'вольная : д, ж, м', 'Рифма': 'вольная', 'Дополнительные параметры': 'нарушения внутренней анакрусы, цезурные наращения, нарушения анакрусы', 'Метрическая формула': 'Дк3,4д,ж,м; Дк2ж', 'Предложений': '5', 'Словоформ': '86'}
    """

GR_TAGS_INFO = \
    """
Поиск по подкорпусу:
    Жанр текста (doc_genre_fi):
        стихотворение
        акростих
        аполог
        ария
        баллада
        басня
        былина
        в альбом
        гимн
        глосса
        дифирамб
        дума
        духовный стих
        загадка
        идиллия
        кантата
        канцона
        касыда
        колыбельная
        куплеты
        мадригал
        марш
        молитва
        надпись
        ода
        оратория
        палиндром
        пародия
        песня
        перевод
        подражание
        посвящение
        послание
        притча
        псалом
        романс
        сатира
        сказка
        стансы
        стихира
        сцена
        танка
        хор
        центон
        цикл
        частушка
        эклога
        экспромт
        элегия
        эпиграмма
        эпиталама
        эпитафия
        эпод
        пьеса
        драма
        комедия
        трагедия
        поэма
        роман в стихах
    Язык оригинала (doc_language):
        английский
        арабский
        белорусский
        венгерский
        датский
        древнегреческий
        древнееврейский
        древнерусский
        испанский
        итальянский
        китайский
        латинский
        немецкий
        новогреческий
        персидский
        польский
        португальский
        провансальский
        сербский
        украинский
        французский
        церковнославянский
        чешский
    Метр (doc_meter):
        Силлабо-тонический
            Хорей: Х
            Ямб: Я
            Дактиль: Д
            Амфибрахий: Аф
            Анапест: Ан
            Гетерометрия: Гетерометрия
        Несиллабо-тонический
            Силлабический: силлабический
            Тонический: тонический
            Гекзаметр: Гек
            Пентаметр: Пен
            Логаэд: логаэд
            Дольник: Дк
            Тактовик: Тк
            Акцентный: Ак
            Свободный(верлибр): Вл
    Число стоп/иктов/слогов (doc_feet):
        Отсутствует: 0
        1
        2
        3
        4
        5
        6
        6
        8
        11
        12
        13
        вольная
        3 4
        4,5
        4,6
        4,5,6
        3,4,5,6
        3,4,6
        регулярная
        4+2
        4+3
        6+3
        6+4
        5+4
    Клауза (doc_clausula):
        вольная
        ж, м
        д, м
        д, ж
        д, ж, м
        г, д
        г, ж
        г, м
        г, д, ж
        г, д, м
        г, ж, м
        г, д, ж, м
        регулярная
        жм
        мж
        жжм
        ммж
        жжмм
        ммжж
        мжжм
        жммж
        мжжм жммж
        жммж мжжм
        жмжжм
        м
        ж
        д
        г
    Строфика (doc_strophe):
        Отсутствует: 0
        александрийский стих
        газелла
        моностих
        нона
        одическая строфа
        децима
        октава
        онегинская строфа
        пантум
        сицилиана
        сонет
        венок сонетов
        терцина
        ритурнель
        триолет
        рондель
        рондо
        рубаи
        баллада
        спенсерова строфа
        канцона
        сапфическая строфа
        алкеева строфа
        элегический дистих
        1
        2
        3
        4
        5
        6
        7
        8
        9
        10
        11
        12
    Графическая строфика (doc_strophe_gr):
        Отсутствует: 0
        вольная
        мнимая проза
        парцеллированная
        сложная
        Длина графических строф:
            2
            3
            4
            5
            6
            8
            10
            12
            16
            18
    Рифма (doc_rhyme):
        Отсутствует(белый стих): 0
        монорим
        спорадическая
        вольная
        регулярная
        Перекрестная(абаб): перекрестная
        Парная(аа): парная
        Тройная(ааа): тройная
        Четверная(аааа): четверная
        Скользящая(абв абв или абвг абвг или подобная): скользящая
        Охватная(абба): охватная
        Четная(хаха): четная
        Нечетная(ахах): нечетная
        Затянутая(любая 5- или 6-строчная строфа на две рифмы): затянутая
        Цепная(терцины или подобная): цепная
        Сложная(иные типы): сложная
        ааб ввб
        абааб
        абаб вв
        абаб ввгг
        абаб вггв
        абабаб
        абабаб вв
    Дополнительные параметры (doc_extra):
        Полиметрия:
            полиметрия
            полиметрический фрагмент
            с полиметрическими фрагментами
            скользящий переход
            упрощенная разметка
        Преобразования метра:
            перебои
            цезурные наращения
            цезурные усечения
            переменная анакруса
            нарушения анакрусы
            нарушения внутренней анакрусы
            урегулированная анакруса
            сверхдлинная анакруса
            нарушение ударной константы
        Особенности строфики:
            нарушения строфики
            усеченная строка
            холостая строка
            белая строка
            кода
            рекурсивная строфика
            рефрен
            редупликация
            строчный логаэд
            прозаические фрагменты
            магистрал
        Особенности рифм:
            тавторифма
            омонимическая рифма
            монотонная рифма
            внутренняя рифма
            разноударная рифма
            неравносложная рифма
            составная рифма
            ассонанс
            диссонанс
            корневая рифма
            начальная рифма
        Особенности метров:
            пеон I
            пеон II
            пеон III
            пеон IV
            пентон
            гиперпентон
            пеонический дольник
            логаэдический дольник
        Прочее:
            внутрисловный перенос
    Формула (s_sp_frm_sch):
        Формула строки совпадает со стандартной стиховедческой записью: метр + количество стоп/иктов/слогов + клаузула, например, Я6д.
        Также тонические и силлабо-тонические строки можно искать по схеме расположения иктов, например, 0*2*1*1*0
"""

TEST_DATA = {'test_single_query': {'query': 'мост'},
             'test_multi_query': {'query': ['мост', 'скала']}
             }


class PageParser(Container):
    def __init__(self, *args, stress=False, exact=True, markup=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.__page = 0
        self.__stress = stress
        self.__exact = exact
        self.__markup = markup

        self.__pattern = re.compile('(\s*[,?!\.:;―\-«»\"\'\'\[\]\(\)]+\s*)')

        self.__subcorp_url = 'https://processing.ruscorpora.ru/search.xml?env=alpha&mode=poetic&sort=i_grtagging&lang=ru&spd=1&text=meta&is_subcorpus=1&dpp=50&'

        if self.query:
            self.__ana_url = 'https://processing.ruscorpora.ru/explain.xml?env=alpha&api=1.0&mycorp=&mysent=&mysize=&mysentsize=&dpp=&spp=&spd=&ct=&mydocsize=&mode=poetic&lang=ru&sort=i_grtagging&nodia=1&&ext=10&req=&text=word-info&language=ru&source='
        else:
            self.__ana_url = 'https://processing.ruscorpora.ru/explain.xml?p=0&nodia=1&&sid=0&&expand=full&is_subcorpus=1&mode=poetic&expdiap=29&text=document-info&language=ru&docid='

        if self.__exact:
            self.__url = 'https://processing.ruscorpora.ru/search.xml?env=alpha&api=1.0&mycorp={}&mysent=&mysize=&mysentsize=&dpp=&spp=&spd=&ct=&mydocsize=&mode=poetic&lang=ru&sort=i_grtagging&nodia={}&text=lexform&ext=10&req={}&p={}'
        else:
            self.__url = 'https://processing.ruscorpora.ru/search.xml?env=alpha&api=1.0&mycorp={}&mysent=&mysize=&mysentsize=&dpp=&spp=&spd=&ct=&mydocsize=&mode=poetic&lang=ru&sort=i_grtagging&nodia={}&text=lexgramm&ext=10&parent1=0&level1=0&lex1=%{}&gramm1=&sem-mod1=sem&sem-mod1=semx&sem1=&form1=&flags1=&p={}&'

    @staticmethod
    def isStartComment(text):
        return (isinstance(text, Comment) and
                text.strip().startswith('trim_up.html start'))

    @staticmethod
    def isEndComment(text):
        return (isinstance(text, Comment) and
                text.strip().startswith('trim_down.html start'))

    @staticmethod
    def get_idxs(sent_list, word, word_id):
        if len(' '.join(sent_list[:word_id])) != 0:
            left = len(' '.join(sent_list[:word_id])) + 1
        else:
            left = 0
        right = left + len(word)
        return (left, right)

    def __parse_sub_dict(self):
        """
        return: subcorpus parameters part of the subcorp_url
        """
        subcorp = ''
        if self.subcorpus:
            for key, value in self.subcorpus.items():
                subcorp += key + '=' + '|'.join(value) + '&'
        return subcorp

    def __get_subcorp(self):
        req = requests.get(self.__subcorp_url + self.__parse_sub_dict() + f'&p={self.__page}')
        soup = BeautifulSoup(req.content, 'html.parser')
        return soup

    def __clean_soup(self, soup):
        """
        A function removing NoneType lines from soup
        """
        if not self.__markup:
            for elem in soup.findAll('td', class_='frm'):
                elem.extract()
        for elem in soup.findAll('td', width='100%'):
            elem.replaceWithChildren()
        for elem in soup.findAll('tr'):
            elem.replaceWithChildren()
        for elem in soup.findAll('br'):
            elem.replaceWithChildren()
        return soup

    def __get_page(self, page_number, value):
        """
        return: etree of the page
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        if self.subcorpus is None:
            subcorp = ''
        else:
            subcorp_soup = self.__get_subcorp()
            subcorp = parse.parse_qs(parse.urlsplit(subcorp_soup.find("a", string="English")['href']).query)['mycorp'][
                0]
        second_part_url = ''
        if not self.__exact:
            if len(self.query.split()) > 1:
                for query_item in range(2, len(self.query.split()) + 1):
                    second_part_url += f'parent{query_item}=0&level{query_item}=0&min{query_item}=1&max{query_item}=1&lex{query_item}={self.query.split()[query_item - 1]}&gramm=&sem-mod{query_item}=sem&sem-mod{query_item}=semx&sem{query_item}=&form{query_item}=&flags{query_item}=&'
        req = requests.get(self.__url.format(subcorp, value, self.query.split()[0], page_number) + second_part_url,
                           headers=headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        self.__clean_soup(soup)
        return soup

    def __ana(self, source):
        """
        A word's analysis parser
        """
        ana = {}

        time.sleep(randint(1, 2))
        req = requests.get(self.__ana_url + source)
        if req.status_code == 429:
            time.sleep(10)
            req = requests.get(self.__ana_url + source)
        soup = BeautifulSoup(req.content, 'html.parser')
        for elem in soup.findAll('br'):
            elem.replaceWithChildren()
        if self.query:
            start = 1
        else:
            start = 0
        for row in soup.find_all('tr')[start:]:
            if row.find_all('td')[-1].attrs and row.find_all('td')[-1].attrs['class'] == ['value']:
                name = row.find_all('td')[0](text=True)[0]
                value = row.find_all('td')[1](text=True)[0]
                if str(name) in ana:
                    break
                else:
                    ana[str(name)] = str(value).strip()
        return ana

    def __parse_page(self, soup, n_docs, n_results, i):
        """
        Function for getting texts with target words
        :return: list of docs
        """
        sent = []
        texts = []
        query_list = []
        ana_list = []
        doc = {}
        count = 0
        for isStartComment in soup.find_all(text=self.isStartComment)[:int(n_docs)]:
            if n_results == 0:
                break
            i += 1
            meta = isStartComment.find_previous('span', class_='b-doc-expl').text.strip()
            for text in isStartComment.find_all_next(text=True):

                if self.isEndComment(text):
                    isEnd = soup.find_all(text=self.isEndComment)[i]
                    previous = isEnd.find_previous('span')
                    while 'trim_up.html end' not in str(previous):
                        if isinstance(previous, Tag):
                            count -= 1
                            if previous.attrs['class'][-1] == 'g-em':
                                query_list.append([previous.text, count])
                                if self.get_analysis:
                                    ana_list.append(self.__ana(previous.attrs['explain']))
                                if len(query_list) == len(self.query.split()):
                                    n_results -= 1
                                    query_list.reverse()
                                    ana_list.reverse()
                                    query = ' '.join(query_list[i][0] for i in range(len(query_list)))
                                    doc['idxs'] = self.get_idxs(sent, query, query_list[0][1])
                                    doc['meta'] = meta
                                    doc['text'] = ' '.join(sent)
                                    doc['analysis'] = ana_list
                                    texts.append(doc)
                                    doc = {}
                                    ana_list = []
                                    query_list = []
                                if n_results == 0:
                                    break
                        if previous is None:
                            break
                        previous = previous.previous_sibling
                    sent = []
                    count = 0
                    break

                elif isinstance(text, Comment):
                    continue

                elif not text.strip():
                    continue

                elif self.__pattern.match(text):
                    if sent:
                        sent[-1] = sent[-1] + text.strip()
                    else:
                        sent.append(text)
                else:
                    sent.append(text.strip().replace(u'\xa0', u' '))

        return texts

    def __parse_text_page(self, link):
        """
        Parser for text pages when query is empty
        """
        req = requests.get(link)
        time.sleep(randint(1, 2))
        if req.status_code == 429:
            print('waiting 10 sec')
            time.sleep(10)
            print('done waiting')
            req = requests.get(link)
        soup = BeautifulSoup(req.content, 'html.parser')
        soup = self.__clean_soup(soup)

        sent = []
        doc = {}
        Start = soup.find(text=self.isStartComment)
        for text in Start.find_all_next(text=True):
            if self.isEndComment(text):
                break
            if isinstance(text, Comment):
                continue
            if not text.strip():
                continue
            if self.__pattern.match(text):
                if sent:
                    sent[-1] = sent[-1] + text.strip()
                else:
                    sent.append(text)
            else:
                sent.append(text.strip())
        doc['text'] = ' '.join(sent)
        doc['meta'] = soup.find(class_='b-doc-expl').text.strip()
        doc['idxs'] = (0, 0)
        if self.get_analysis:
            doc['analysis'] = self.__ana(soup.find(class_='b-doc-expl')['explain'])
        else:
            doc['analysis'] = []
        return doc

    def __get_results(self):
        texts = []
        if self.query:
            if self.__stress:
                value = 0
            else:
                value = 1

            while self.n_results != 0:
                soup = self.__get_page(self.__page, value)
                self.__page += 1
                if len(soup.find_all(text=self.isStartComment)) == 0:
                    break
                elif self.n_results >= len(soup.find_all(class_='b-wrd-expl g-em')) / len(self.query.split()):
                    i = -1
                    texts.extend(self.__parse_page(soup, len(soup.find_all(text=self.isStartComment)),
                                                   len(soup.find_all(class_='b-wrd-expl g-em')), i))
                    self.n_results -= (len(soup.find_all(class_='b-wrd-expl g-em')) / len(self.query.split()))
                else:
                    i = -1
                    texts.extend(self.__parse_page(soup, self.n_results, self.n_results, i))
                    self.n_results = 0
        else:
            while self.n_results != 0:
                subcorp_soup = self.__get_subcorp()
                self.__page += 1
                if self.n_results >= len(subcorp_soup.find_all(class_='b-kwic-expl')):
                    self.n_results -= len(subcorp_soup.find_all(class_='b-kwic-expl'))
                    for text in subcorp_soup.find_all(class_='b-kwic-expl'):
                        if not self.__stress:
                            url_part = text['href']
                        else:
                            url_list = text['href'].split('&')
                            i = url_list.index('nodia=1')
                            url_list[i] = 'nodia=0'
                            url_part = '&'.join(url_list)
                        texts.append(self.__parse_text_page('https://processing.ruscorpora.ru' + url_part))

                else:
                    for text in subcorp_soup.find_all(class_='b-kwic-expl')[:self.n_results]:
                        if not self.__stress:
                            url_part = text['href']
                        else:
                            url_list = text['href'].split('&')
                            i = url_list.index('nodia=1')
                            url_list[i] = 'nodia=0'
                            url_part = '&'.join(url_list)
                        texts.append(self.__parse_text_page('https://processing.ruscorpora.ru' + url_part))
                    self.n_results = 0

        return texts

    def extract(self):
        """
        A streamer to Corpus
        """
        docs = self.__get_results()
        for doc in docs:
            yield Target(doc['text'], doc['idxs'], doc['meta'], doc['analysis'])
