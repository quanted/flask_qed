import unittest
import sip_model_rest

class TestSip(unittest.TestCase):
	def setup(self):
		#setup the test as needed
		#e.g. pandas to open sip qaqc csv
		pass

	def teardown(self):
		#teardown called after each test
		#e.g. maybe write test results to some text file
		pass

	def test_fail(self):
		result = [1,2,3]
		self.assertEquals(result, [2,3,4])

	def test_pass(self):
		result = [2,3,4]
		self.assertEquals(result, [2,3,4])

	def test_sip_blackbox(self):
		pass
		#setup sip object
		#compare sip qaqc csv expected output to
		#sip object output with an asserEquals

#unittest will 
#1) call the setup method, 
#2) then call every method starting with "test", 
#3) then the teardown method
if __name__ == '__main__':
	unittest.main()
