import pytest
from scripts.rect import Rect

# The setup method is called before each test method in the test class.
# The teardown method is called after each test method in the test class.


# Test rect with function
def test_rect_one(rect: Rect):

    #rect = Rect(0, 0, 10, 10)
    assert rect.left == 0

def test_rect_two(rect: Rect):
    
    #rect = Rect(0, 0, 10, 10)
    assert rect.right == 10

# Test rect with class
class TestRect:

    def setup_method(self, method):
        print(f'\n{method.__name__}()')
        self.rect = Rect(0, 0, 10, 10)

    def teardown_method(self, method):
        print(f'{method.__name__}()') 

    def test_one(self):

        assert self.rect.left == 0