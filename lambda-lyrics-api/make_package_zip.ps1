rm package.zip
rm package -r
pip install -r ./requirements.txt --target ./package
cp scrape.py package/scrape.py
cp search.py package/search.py
cp make_response.py package/make_response.py
Compress-Archive ./package/* package.zip
rm package -r
