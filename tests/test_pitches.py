from app.models import User, Pitch
import unittest

class PitchModelTest(unittest.TestCase):
    def setUp(self):
        self.user_Peris = User(username = 'Peris',pass_secure = 'banana', email = 'james@ms.com')
        self.new_pitch = Pitch(id=1,p_title='Test',p_body='This is a test pitch',category="employee",user = self.user_Peris,upvote=0,downvote=0)

    def tearDown(self):
        User.query.delete()
        Pitch.query.delete()
      

    def test_check_instance_variables(self):
        self.assertEquals(self.new_pitch.p_title,'Test')
        self.assertEquals(self.new_pitch.p_body,'This is a test pitch')
        self.assertEquals(self.new_pitch.category,"interview")
        self.assertEquals(self.new_pitch.user,self.user_Peris)

    def test_save_pitch(self):
        self.new_pitch.save_pitch()
        self.assertTrue(len(Pitch.query.all())>0)

    def test_get_pitch_by_id(self):
        self.new_pitch.save_pitch()
        got_pitch = Pitch.get_pitch(1)
        self.assertTrue(got_pitch is not None)