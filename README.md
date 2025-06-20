# Langchain based RAG 

---

# Start ElasticSearch service
```bash
cd rag-services
docker-compose up -d
```

---

# How to download documents
```bash
mkdir -p documents/HR/agile
mkdir -p documents/HR/scrum
curl --output "documents/HR/agile/agile-po-prostu-ebook.pdf" --url "https://projectmakers.pl/wp-content/uploads/2024/01/agile-po-prostu-ebook.pdf"
curl --output "documents/HR/scrum/2020-Scrum-Guide-Polish.pdf" --url "https://scrumguides.org/docs/scrumguide/v2020/2020-Scrum-Guide-Polish.pdf"
```

---

# Create env
```bash
python -m venv venv
source venv/bin/activate
# .\venv\activate
pip install -U -r resources.txt
python -m spacy download pl_core_news_md
# rename env to .env
# set OPENAI_API_KEY
```

---

# Ask RAG system
```text
Query: Czym różni się Agile od Scrum'a?
Answer: Agile to metodologia zarządzania projektami, która skupia się na iteracyjnym dostarczaniu wartościowych 
produktów poprzez elastyczne podejście do wymagań i zmian. Scrum jest konkretnym ramem postępowania w ramach Agile, 
zawierającym określone wydarzenia, artefakty i role, które wspierają pracę zespołu i realizację celów. 
Różni się od Agile głównie tym, że jest to szczegółowy framework z jasno określonymi praktykami, 
podczas gdy Agile to bardziej szeroka filozofia i zbiór zasad.

Query: Co to jest Agile?
Answer: Agile to metoda zarządzania projektami oparta na iteracyjnym dostarczaniu działającego oprogramowania, 
elastycznym reagowaniu na zmiany i współpracy z klientem. W praktyce polega na częstym wydawaniu wersji produktu, 
zbieraniu informacji zwrotnej i dostosowywaniu działań. Głównym celem jest tworzenie wartościowych rozwiązań,
skoncentrowanych na rezultacie, a nie tylko na formalnych procedurach.

Query: Co to jest Sprint?
Answer: Sprint to ograniczony czasowo etap w procesie zwinnego zarządzania projektem, podczas którego zespół dąży 
do osiągnięcia konkretnego celu poprzez realizację wybranych elementów backlogu. Trwa zazwyczaj od 1 do 4 tygodni 
i obejmuje planowanie, codzienne spotkania, przegląd wyników oraz retrospekcję. Sprint stwarza warunki do inspekcji 
i adaptacji postępów, zapewnia przewidywalność oraz skupienie na realizacji celu produktu.

Query: Jak duży powinien być zespół w Scrum?
Answer: Zespół w Scrum powinien liczyć maksymalnie około 10 osób, aby pozostać zwinny i skuteczny. 
Mniejsze zespoły lepiej się komunikują i są bardziej produktywne. Jeśli zespół staje się zbyt liczny, 
warto rozważyć podział na kilka spójnych Scrum Teamów skupionych na tym samym Produkcie.

Query: Jak duży powinien być zespół w Agile?
Answer: W Agile, szacowanie prac według Story Points jest preferowane, ponieważ nie są one bezpośrednio powiązane 
z czasem i pozwalają na bardziej elastyczne planowanie. Pomaga to w ocenie złożoności zadań i ich zakresu 
w sposób niezależny od dokładnego określenia czasu. Szacowanie w jednostkach czasu (np. godzinach) może być
mniej skuteczne, gdyż nie odzwierciedla rzeczywistej złożoności pracy i może sprzyjać niepotrzebnej precyzji.

Query: Jakie jest zadanie Scrum Master'a?
Answer: Zadanie Scrum Master'a polega na tworzeniu i wspieraniu środowiska sprzyjającego efektywnemu stosowaniu Scruma,
pomagając zespołowi i organizacji zrozumieć i stosować jego zasady, a także zapewniając efektywność zespołu. 
Jego obowiązki obejmują wspieranie w inspekcji i adaptacji procesów, ułatwianie wyd
arzeń scrumowych oraz rozwiązywanie barier, aby zespół mógł tworzyć wartościowe przyrosty. W skrócie, Scrum Master 
dba o to, aby Scrum był prawidłowo wdrożony i funkcjonował zgodnie z jego ramami, wspierając zespół i organizację.
```

# Ask RAG system with chat
```text
Query: Czym różni się Agile od Scrum'a?
Answer: Agile to ogólna filozofia i zbiór wartości, które promują elastyczność, współpracę i szybkie dostarczanie wartości, 
natomiast Scrum jest konkretnym ramem postępowania (framework) opartym na tej filozofii, z jasno określonymi rolami, 
wydarzeniami i artefaktami. Scrum jest jednym ze sposobów realizacji zasad Agile, skupiając się na iteracyjnym i 
przyrostowym rozwoju, podczas gdy Agile to szeroki zbiór praktyk i wartości. Różni się więc poziomem ogólności: 
Agile jest koncepcją, a Scrum konkretnym narzędziem do jej wdrażania.

Query: Co to jest Agile?
Answer: Agile to metoda zarządzania projektami oparta na częstym wydawaniu działających wersji oprogramowania 
i zbieraniu informacji zwrotnej. Skupia się na celach, które chce się osiągnąć, i na tym, jak znaleźć odpowiednie 
rozwiązania, z zachowaniem elastyczności wobec zmian. Kluczowe elementy to ludzie, interakcje, działające oprogramowanie, 
współpraca z klientem i reakcja na zmiany.

Query: Co to jest Sprint?
Answer: Sprint to planowane wydarzenie o ustalonej długości, trwające maksymalnie miesiąc, podczas którego skupia się 
na realizacji określonych celów. Rozpoczyna się natychmiast po zakończeniu poprzedniego i obejmuje pracę 
nad osiągnięciem celu Sprintu, czyli konkretnego kroku w realizacji Produktu. W trakcie Sprintu nie wprowadza się zmian, 
które zagrażałyby celu, a praca jest inspekowana i adaptowana zgodnie z potrzebami.

Query: Jak duży powinien być zespół w Scrum?
Answer: W Scrum, optymalny rozmiar zespołu deweloperskiego wynosi zazwyczaj od 3 do 9 osób. Taki rozmiar pozwala
na skuteczną komunikację, współpracę oraz elastyczność w realizacji zadań. Zespół ten nazywany jest Scrum Team 
i składa się z trzech ról: Product Owner, Scrum Master oraz Zespół Deweloperski. Najważniejsze jest, aby zespół był 
wystarczająco mały, by mógł działać zwinie i szybko się komunikować, jednocześnie na tyle duży, 
by realizować kompleksowe zadania i dostarczać wartość.

Query: Jak duży powinien być zespół w Agile?
Answer: W Agile nie ma jednej idealnej wielkości zespołu, ponieważ optymalna liczba zależy od wielu czynników, 
takich jak projekt, zakres prac i dostępne zasoby. Jednakże, zgodnie z najlepszymi praktykami, zespoły Agile 
zwykle składają się z 5 do 9 członków. Taki rozmiar pozwala na efektywną komunikację, współpracę i szybką reakcję 
na zmiany, jednocześnie umożliwiając zachowanie autonomii i elastyczności zespołu.Czy chcesz, abym znalazł szczegółowe 
źródła lub wytyczne na ten temat?

Query: Jakie jest zadanie Scrum Master'a?
Answer: Scrum Master odpowiada za to, aby Scrum był stosowany zgodnie z opisem w przewodniku, pomagając wszystkim 
w zrozumieniu teorii i praktyki Scrum. Ponosi też odpowiedzialność za efektywność Scrum Teamu, tworząc odpowiednie 
warunki do poprawy praktyk i wspierając jego działania. Scrum Master pełni rolę lidera wspierającego, działając 
na rzecz organizacji i zespołu.
```

# Documentation
```text
RAG
https://python.langchain.com/docs/tutorials/rag/
https://python.langchain.com/docs/tutorials/qa_chat_history/

Elasticsearch
https://python.langchain.com/docs/integrations/vectorstores/elasticsearch/
https://python.langchain.com/docs/integrations/retrievers/elasticsearch_retriever/

MultiQueryRetriever
https://python.langchain.com/docs/how_to/MultiQueryRetriever/
```