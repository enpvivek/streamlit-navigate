import streamlit as st
import streamlit_shadcn_ui as ui
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer


indexName = "all_products"
indexName1="all_productsp"
indexName2="all_productsps"

try:
    es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "divij23"),
    #ca_certs="/Users/Suresh Babu/elasticsearch-8.13.2/config/certs/http_ca.crt"
    )
except ConnectionError as e:
    print("Connection Error:", e)
    
if es.ping():
    print("Succesfully connected to ElasticSearch!!")
else:
    print("Oops!! Can not connect to Elasticsearch!")




def search(input_keyword):
    model = SentenceTransformer('all-mpnet-base-v2')
    vector_of_input_keyword = model.encode(input_keyword)

    query = {
        "field": "DescriptionVectorV",
        "query_vector": vector_of_input_keyword,
        "k": 10,
        "num_candidates": 500
    }
    res = es.knn_search(index="all_productsp"
                        , knn=query 
                        , source=["Job Title","Job Description"]
                        )
    results = res["hits"]["hits"]

    return results

def search1(input_keyword):
    model = SentenceTransformer('all-mpnet-base-v2')
    vector_of_input_keyword = model.encode(input_keyword)

    query = {
        "field": "DescriptionVector",
        "query_vector": vector_of_input_keyword,
        "k": 10,
        "num_candidates": 500
    }
    res = es.knn_search(index="all_products"
                        , knn=query 
                        , source=["ProductName","Description"]
                        )
    results = res["hits"]["hits"]

    return results

def search2(input_keyword):
    model = SentenceTransformer('all-mpnet-base-v2')
    vector_of_input_keyword = model.encode(input_keyword)

    query = {
        "field": "DescriptionVectorV1",
        "query_vector": vector_of_input_keyword,
        "k": 10,
        "num_candidates": 500
    }
    res = es.knn_search(index="all_productsps"
                        , knn=query 
                        , source=["college","review"]
                        )
    results = res["hits"]["hits"]

    return results

def main():
    st.title("Search")
    st.sidebar.success("Start searching through NavigateNet.")
    
    if "my_input" not in st.session_state:
        st.session_state["my_input"] = ""

    choice = ui.select(options=["job", "Academics", "Fashion"])

    st.markdown(f"Current Searching Domain: {choice}")

    # Input: User enters search query
    search_query = ui.input( type='text', placeholder="Enter your Search Query", key="input1")

    # Button: User triggers the search
    if st.button("Search"):
        if search_query:
            if choice=="job":
                # Perform the search and get results
                results = search(search_query)

                # Display search results
                st.subheader("Search Results")
                for result in results:
                    with st.container():
                        if '_source' in result:
                            try:
                                st.header(f"{result['_source']['Job Title']}")
                            except Exception as e:
                                print(e)
                            try:
                                st.write(f"Company Name: {result['_source']['Company Name']}")
                            except Exception as e:
                                print(e)
                            try:
                                st.write(f"Job Description: {result['_source']['Job Description']}")
                            except Exception as e:
                                print(e)
                            st.divider()
            elif  choice=="Fashion":
                # Perform the search and get results
                results = search1(search_query)

                # Display search results
                st.subheader("Search Results")
                for result in results:
                    with st.container():
                        if '_source' in result:
                            try:
                                st.header(f"{result['_source']['ProductName']}")
                            except Exception as e:
                                print(e)
                            try:
                                st.write(f"Product details: {result['_source']['Description']}")
                            except Exception as e:
                                print(e)
                            st.divider()

            else :
                # Perform the search and get results
                results = search2(search_query)

                # Display search results
                st.subheader("Search Results")
                for result in results:
                    with st.container():
                        if '_source' in result:
                            try:
                                st.header(f"{result['_source']['college']}")
                            except Exception as e:
                                print(e)
                            try:
                                st.write(f"Details: {result['_source']['review']}")
                            except Exception as e:
                                print(e)
                            st.divider()

                    
if __name__ == "__main__":
    main()



