from django.utils.unittest import skipIf
import warnings
from django.test import TestCase
from careful_forms.conf import settings
from careful_forms.middleware import SecurityWarning
from careful_forms.tests.forms import (
    NormalForm, NormalCorrectModelForm, NormalIncorrectModelForm,
    CarefullyfiedForm, CarefullyfiedCorrectModelForm,
    CarefullyfiedIncorrectModelForm
)


@skipIf(not settings.CAREFUL_ENABLED, "Skipping because CarefulForms are disabled")
class CarefulFormsTests(TestCase):
    def test_sanity_1(self):
        form = NormalForm()
        self.assertEqual(str(form), '<tr><th><label for="id_name">Name:</label></th><td><input id="id_name" type="text" name="name" maxlength="200" /></td></tr>\n<tr><th><label for="id_email">Email:</label></th><td><input id="id_email" type="text" name="email" maxlength="200" /></td></tr>\n<tr><th><label for="id_dangerous_field">Dangerous field:</label></th><td><input id="id_dangerous_field" type="text" name="dangerous_field" maxlength="200" /></td></tr>')

    def test_sanity_2(self):
        form = NormalCorrectModelForm()
        self.assertEqual(str(form), '<tr><th><label for="id_name">Name:</label></th><td><input id="id_name" type="text" name="name" maxlength="200" /></td></tr>\n<tr><th><label for="id_email">Email:</label></th><td><input id="id_email" type="text" name="email" maxlength="200" /></td></tr>')

    def test_sanity_3(self):
        form = NormalIncorrectModelForm()
        self.assertEqual(str(form), '<tr><th><label for="id_name">Name:</label></th><td><input id="id_name" type="text" name="name" maxlength="200" /></td></tr>\n<tr><th><label for="id_email">Email:</label></th><td><input id="id_email" type="text" name="email" maxlength="200" /></td></tr>\n<tr><th><label for="id_dangerous_field_2">Dangerous field 2:</label></th><td><input type="checkbox" name="dangerous_field_2" id="id_dangerous_field_2" /></td></tr>')

    def test_careful_form_1(self):
        form = CarefullyfiedForm()
        self.assertEqual(str(form), '<tr><th><label for="id_name">Name:</label></th><td><input id="id_name" type="text" name="name" maxlength="200" /></td></tr>\n<tr><th><label for="id_email">Email:</label></th><td><input id="id_email" type="text" name="email" maxlength="200" /></td></tr>\n<tr><th><label for="id_dangerous_field">Dangerous field:</label></th><td><input id="id_dangerous_field" type="text" name="dangerous_field" maxlength="200" /></td></tr>')
        self.assertEqual(form.not_accessed_fields, set())

    def test_careful_form_2(self):
        form = CarefullyfiedForm()
        _ = form['name']
        _ = form['email']
        self.assertEqual(form.not_accessed_fields, set(('dangerous_field',)))

    def test_careful_form_3(self):
        form = CarefullyfiedForm()
        _ = form.fields['name']
        _ = form.fields['email']
        self.assertEqual(form.not_accessed_fields, set(('dangerous_field',)))

    def test_careful_form_4(self):
        form = CarefullyfiedForm()
        _ = form.fields.get('name')
        _ = form.fields.get('email')
        self.assertEqual(form.not_accessed_fields, set(('dangerous_field',)))

    def test_careful_form_5(self):
        form = CarefullyfiedForm()
        form.fields.keys()
        self.assertEqual(form.not_accessed_fields, set())

    def test_careful_form_6(self):
        form = CarefullyfiedForm()
        iterkeys = form.fields.iterkeys()
        self.assertEqual(form.not_accessed_fields, set(('name', 'email', 'dangerous_field')))
        list(iterkeys)
        self.assertEqual(form.not_accessed_fields, set())

    def test_careful_form_7(self):
        form = CarefullyfiedForm()
        iteritems = form.fields.iteritems()
        self.assertEqual(form.not_accessed_fields, set(('name', 'email', 'dangerous_field')))
        list(iteritems)
        self.assertEqual(form.not_accessed_fields, set())

    def test_careful_form_8(self):
        form = CarefullyfiedForm()
        del form.fields
        self.assertEqual(form.not_accessed_fields, set())

    def test_careful_model_form_1(self):
        form = CarefullyfiedCorrectModelForm()
        self.assertEqual(str(form), '<tr><th><label for="id_name">Name:</label></th><td><input id="id_name" type="text" name="name" maxlength="200" /></td></tr>\n<tr><th><label for="id_email">Email:</label></th><td><input id="id_email" type="text" name="email" maxlength="200" /></td></tr>')
        self.assertEqual(form.not_accessed_fields, set())

    def test_careful_model_form_2(self):
        form = CarefullyfiedIncorrectModelForm()
        self.assertEqual(str(form), '<tr><th><label for="id_name">Name:</label></th><td><input id="id_name" type="text" name="name" maxlength="200" /></td></tr>\n<tr><th><label for="id_email">Email:</label></th><td><input id="id_email" type="text" name="email" maxlength="200" /></td></tr>\n<tr><th><label for="id_dangerous_field_2">Dangerous field 2:</label></th><td><input type="checkbox" name="dangerous_field_2" id="id_dangerous_field_2" /></td></tr>')
        self.assertEqual(form.not_accessed_fields, set())

    def test_careful_model_form_3(self):
        form = CarefullyfiedIncorrectModelForm()
        _ = form.fields.get('name')
        _ = form.fields.get('email')
        self.assertEqual(form.not_accessed_fields, set(('dangerous_field_2',)))

    def test_careful_middleware_1(self):
        with warnings.catch_warnings(record=True) as w:
            self.client.get("/form/normal/")
        self.assertEqual(w, [])

    def test_careful_middleware_2(self):
        with warnings.catch_warnings(record=True) as w:
            self.client.get("/form/careful_incorrect/")
        self.assertTrue("warnings.WarningMessage" in str(w))
        self.assertEqual(len(w), 1)
        warning = w[0]
        self.assertEqual(warning.category, SecurityWarning)
        self.assertTrue("dangerous_field_2" in warning.message.message)

    def test_careful_middleware_3(self):
        old_exception_on_warning = settings.CAREFUL_EXCEPTION_ON_WARNING
        settings.CAREFUL_EXCEPTION_ON_WARNING = True
        self.assertRaises(SecurityWarning, self.client.get, "/form/careful_incorrect/")
        settings.CAREFUL_EXCEPTION_ON_WARNING = old_exception_on_warning

    def test_careful_middleware_4(self):
        with warnings.catch_warnings(record=True) as w:
            self.client.get("/form/careful_correct/")
        self.assertEqual(w, [])


@skipIf(settings.CAREFUL_ENABLED, "Skipping because CarefulForms are enabled")
class CarefulFormsTestsDisabled(TestCase):
    def test_careful_form_1(self):
        form = CarefullyfiedForm()
        self.assertEqual(str(form), '<tr><th><label for="id_name">Name:</label></th><td><input id="id_name" type="text" name="name" maxlength="200" /></td></tr>\n<tr><th><label for="id_email">Email:</label></th><td><input id="id_email" type="text" name="email" maxlength="200" /></td></tr>\n<tr><th><label for="id_dangerous_field">Dangerous field:</label></th><td><input id="id_dangerous_field" type="text" name="dangerous_field" maxlength="200" /></td></tr>')
        self.assertEqual(form.not_accessed_fields, set())

    def test_careful_middleware_1(self):
        with warnings.catch_warnings(record=True) as w:
            self.client.get("/form/careful_incorrect/")
        self.assertEqual(w, [])

    def test_careful_middleware_2(self):
        with warnings.catch_warnings(record=True) as w:
            self.client.get("/form/careful_correct/")
        self.assertEqual(w, [])
