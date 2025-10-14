import pytest
import os

@pytest.fixture(autouse=True)
def setup_test_database():
    test_database = "test_library.db"
    os.environ['LIBRARY_DATABASE'] = test_database
    from database import init_database, add_sample_data
    init_database()
    add_sample_data()  
    yield
   
    if os.path.exists(test_database):
        os.remove(test_database)
    del os.environ['LIBRARY_DATABASE']