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