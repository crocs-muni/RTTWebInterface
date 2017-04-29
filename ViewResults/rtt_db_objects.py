from scipy.stats import binom


class Experiment(object):
    table_name = "experiments"
    expected_tuple_els = 10

    def __init__(self, tup):
        check_init_tuple(tup, Experiment.expected_tuple_els, self.__class__.__name__)

        self.id = tup[0]
        self.name = tup[1]
        self.author_email = tup[2]
        self.status = tup[3]
        self.created = tup[4]
        self.run_started = tup[5]
        self.run_finished = tup[6]
        self.config_file = tup[7]
        self.data_file = tup[8]
        self.data_file_sha256 = tup[9]

    def __str__(self):
        return "{} - ID: {}, Name: {}".format(self.__class__.__name__, self.id, self.name)

    @staticmethod
    def get_all(conn) -> ['Experiment']:
        return get_all_db_objects(conn, Experiment, Experiment.table_name)

    @staticmethod
    def get_all_count(conn) -> int:
        return get_all_count(conn, Experiment.table_name)

    @staticmethod
    def get_by_id(conn, experiment_id) -> 'Experiment':
        return get_db_object_by_primary_id(conn, Experiment, Experiment.table_name, experiment_id)

    @staticmethod
    def get_some(conn, offset, count, id_ord_desc=True):
        select_stmt = "SELECT * FROM {} ORDER BY id".format(Experiment.table_name)
        if id_ord_desc:
            select_stmt += " DESC"
        select_stmt += " LIMIT %s, %s"

        with conn.cursor() as c:
            c.execute(select_stmt, (offset, count, ))
            if c.rowcount == 0:
                return []
            return map_db_rows_to_objects(c.fetchall(), Experiment)

    @staticmethod
    def get_all_filtered(conn, *args, **kwargs) -> ['Experiment']:
        first = True
        arg_list = []

        id_ord_desc = kwargs.pop('id_ord_desc', True)
        name = kwargs.pop('name')
        email = kwargs.pop('email')
        created_from = kwargs.pop('created_from')
        created_to = kwargs.pop('created_to')
        sha256 = kwargs.pop('sha256')

        # Building the query
        query = "SELECT * FROM {} WHERE".format(Experiment.table_name)
        if name is not None and len(name) > 0:
            first = False
            query += " name LIKE %s"
            arg_list.append("%" + name + "%")

        if email is not None and len(email) > 0:
            if not first:
                query += " AND"
            else:
                first = False
            query += " author_email = %s"
            arg_list.append(email)

        if created_from is not None:
            if not first:
                query += " AND"
            else:
                first = False
            query += " created >= %s"
            arg_list.append(created_from)

        if created_to is not None:
            if not first:
                query += " AND"
            else:
                first = False
            query += " created <= %s"
            arg_list.append(created_to)

        if sha256 is not None and len(sha256) > 0:
            if not first:
                query += " AND"
            query += " data_file_sha256 = %s"
            arg_list.append(sha256)

        query += " ORDER BY id"
        if id_ord_desc:
            query += " DESC"

        if len(arg_list) == 0:
            return None

        with conn.cursor() as c:
            c.execute(query, arg_list)
            if c.rowcount == 0:
                return []
            return map_db_rows_to_objects(c.fetchall(), Experiment)


class Job(object):
    table_name = "jobs"
    foreign_id_column = "experiment_id"
    expected_tuple_els = 6
    
    def __init__(self, tup):
        check_init_tuple(tup, Job.expected_tuple_els, self.__class__.__name__)

        self.id = tup[0]
        self.battery = tup[1]
        self.status = tup[2]
        self.run_started = tup[3]
        self.run_finished = tup[4]
        self.experiment_id = tup[5]

    def __str__(self):
        return "{} - ID: {}, Battery: {}, Experiment ID: {}".format(self.__class__.__name__, self.id,
                                                                    self.battery, self.experiment_id)

    @staticmethod
    def get_all(conn) -> ['Job']:
        return get_all_db_objects(conn, Job, Job.table_name)

    @staticmethod
    def get_by_id(conn, job_id) -> 'Job':
        return get_db_object_by_primary_id(conn, Job, Job.table_name, job_id)

    @staticmethod
    def get_by_experiment_id(conn, experiment_id) -> ['Job']:
        return get_db_objects_by_foreign_id(conn, Job, Job.table_name,
                                            experiment_id, Job.foreign_id_column)


class Battery(object):
    table_name = "batteries"
    foreign_id_column = "experiment_id"
    expected_tuple_els = 6

    def __init__(self, tup):
        check_init_tuple(tup, Battery.expected_tuple_els, self.__class__.__name__)

        self.id = tup[0]
        self.name = tup[1]
        self.passed_tests = tup[2]
        self.total_tests = tup[3]
        self.alpha = tup[4]
        self.experiment_id = tup[5]

    def __str__(self):
        return "{} - ID: {}, Name: {}, Experiment ID: {}".format(self.__class__.__name__, self.id,
                                                                 self.name, self.experiment_id)

    def total_passed_diff(self):
        return self.total_tests - self.passed_tests

    def get_prob_of_random(self):
        # We calculate with alpha=0.01
        # Therefore probability of test passing is 0.99
        return binom.pmf(self.passed_tests, self.total_tests, 1 - 0.01)

    def get_assessment(self):
        if self.total_tests == 0:
            return ""

        eps = 1e-8
        p = self.get_prob_of_random()
        if p < 0.001 - eps:
            return "FAIL"
        elif p < 0.01 - eps:
            return "Suspect"
        else:
            return "OK"

    @staticmethod
    def get_all(conn) -> ['Battery']:
        return get_all_db_objects(conn, Battery, Battery.table_name)

    @staticmethod
    def get_by_id(conn, battery_id) -> 'Battery':
        return get_db_object_by_primary_id(conn, Battery, Battery.table_name, battery_id)

    @staticmethod
    def get_by_experiment_id(conn, experiment_id) -> ['Battery']:
        return get_db_objects_by_foreign_id(conn, Battery, Battery.table_name,
                                            experiment_id, Battery.foreign_id_column)


class BatteryError(object):
    table_name = "battery_errors"
    foreign_id_column = "battery_id"
    expected_tuple_els = 3

    def __init__(self, tup):
        check_init_tuple(tup, BatteryError.expected_tuple_els, self.__class__.__name__)

        self.id = tup[0]
        self.message = tup[1]
        self.battery_id = tup[2]

    def __str__(self):
        return "{} - ID: {}, Message: {}, Battery ID: {}".format(self.__class__.__name__, self.id,
                                                                 self.message, self.battery_id)

    @staticmethod
    def get_all(conn) -> ['BatteryError']:
        return get_all_db_objects(conn, BatteryError, BatteryError.table_name)

    @staticmethod
    def get_by_id(conn, battery_error_id) -> 'BatteryError':
        return get_db_object_by_primary_id(conn, BatteryError, BatteryError.table_name, battery_error_id)

    @staticmethod
    def get_by_battery_id(conn, battery_id) -> ['BatteryError']:
        return get_db_objects_by_foreign_id(conn, BatteryError, BatteryError.table_name,
                                            battery_id, BatteryError.foreign_id_column)


class BatteryWarning(object):
    table_name = "battery_warnings"
    foreign_id_column = "battery_id"
    expected_tuple_els = 3

    def __init__(self, tup):
        check_init_tuple(tup, BatteryWarning.expected_tuple_els, self.__class__.__name__)

        self.id = tup[0]
        self.message = tup[1]
        self.battery_id = tup[2]

    def __str__(self):
        return "{} - ID: {}, Message: {}, Battery ID: {}".format(self.__class__.__name__, self.id,
                                                                 self.message, self.battery_id)

    @staticmethod
    def get_all(conn) -> ['BatteryWarning']:
        return get_all_db_objects(conn, BatteryWarning, BatteryWarning.table_name)

    @staticmethod
    def get_by_id(conn, battery_error_id) -> 'BatteryWarning':
        return get_db_object_by_primary_id(conn, BatteryWarning, BatteryWarning.table_name, battery_error_id)

    @staticmethod
    def get_by_battery_id(conn, battery_id) -> ['BatteryWarning']:
        return get_db_objects_by_foreign_id(conn, BatteryWarning, BatteryWarning.table_name,
                                            battery_id, BatteryWarning.foreign_id_column)


class Test(object):
    table_name = "tests"
    foreign_id_column = "battery_id"
    expected_tuple_els = 6

    def __init__(self, tup):
        check_init_tuple(tup, Test.expected_tuple_els, self.__class__.__name__)

        self.id = tup[0]
        self.name = tup[1]
        self.partial_alpha = tup[2]
        self.result = tup[3]
        self.test_index = tup[4]
        self.battery_id = tup[5]

    def __str__(self):
        return "{} - ID: {}, Name: {}, Battery ID: {}".format(self.__class__.__name__, self.id,
                                                              self.name, self.battery_id)

    @staticmethod
    def get_all(conn) -> ['Test']:
        return get_all_db_objects(conn, Test, Test.table_name)

    @staticmethod
    def get_by_id(conn, test_id) -> 'Test':
        return get_db_object_by_primary_id(conn, Test, Test.table_name, test_id)

    @staticmethod
    def get_by_battery_id(conn, battery_id) -> ['Test']:
        return get_db_objects_by_foreign_id(conn, Test, Test.table_name,
                                            battery_id, Test.foreign_id_column)


class Variant(object):
    table_name = "variants"
    foreign_id_column = "test_id"
    expected_tuple_els = 3

    def __init__(self, tup):
        check_init_tuple(tup, Variant.expected_tuple_els, self.__class__.__name__)

        self.id = tup[0]
        self.variant_index = tup[1]
        self.test_id = tup[2]

    def __str__(self):
        return "{} - ID: {}, Index: {}, Test ID: {}".format(self.__class__.__name__, self.id,
                                                            self.variant_index, self.test_id)

    @staticmethod
    def get_result(conn, variant_id) -> str:
        with conn.cursor() as c:
            c.execute(
                "SELECT COUNT(1) "
                "FROM {0} "
                "JOIN {1} "
                "ON {0}.{2}={1}.id "
                "WHERE {0}.result='failed' "
                "AND {1}.{3}=%s"
                .format(Statistic.table_name, Subtest.table_name,
                        Statistic.foreign_id_column, Subtest.foreign_id_column)
                , (variant_id, ))
            if c.fetchone()[0] == 0:
                return "passed"

            return "failed"

    @staticmethod
    def get_all(conn) -> ['Variant']:
        return get_all_db_objects(conn, Variant, Variant.table_name)

    @staticmethod
    def get_by_id(conn, variant_id) -> 'Variant':
        return get_db_object_by_primary_id(conn, Variant, Variant.table_name, variant_id)

    @staticmethod
    def get_by_test_id(conn, test_id) -> ['Variant']:
        return get_db_objects_by_foreign_id(conn, Variant, Variant.table_name,
                                            test_id, Variant.foreign_id_column)

    @staticmethod
    def get_by_test_id_count(conn, test_id) -> int:
        return get_foreign_id_count(conn, Variant.table_name, test_id,
                                    Variant.foreign_id_column)


class VariantError(object):
    table_name = "variant_errors"
    foreign_id_column = "variant_id"
    expected_tuple_els = 3

    def __init__(self, tup):
        check_init_tuple(tup, VariantError.expected_tuple_els, self.__class__.__name__)

        self.id = tup[0]
        self.message = tup[1]
        self.variant_id = tup[2]

    def __str__(self):
        return "{} - ID: {}, Message: {}, Variant ID: {}".format(self.__class__.__name__, self.id,
                                                                 self.message, self.variant_id)

    @staticmethod
    def get_all(conn) -> ['VariantError']:
        return get_all_db_objects(conn, VariantError, VariantError.table_name)

    @staticmethod
    def get_by_id(conn, error_message_id) -> 'VariantError':
        return get_db_object_by_primary_id(conn, VariantError, VariantError.table_name,
                                           error_message_id)

    @staticmethod
    def get_by_variant_id(conn, variant_id) -> ['VariantError']:
        return get_db_objects_by_foreign_id(conn, VariantError, VariantError.table_name,
                                            variant_id, VariantError.foreign_id_column)

    @staticmethod
    def get_by_variant_id_count(conn, variant_id) -> int:
        return get_foreign_id_count(conn, VariantError.table_name, variant_id,
                                    VariantError.foreign_id_column)


class VariantWarning(object):
    table_name = "variant_warnings"
    foreign_id_column = "variant_id"
    expected_tuple_els = 3

    def __init__(self, tup):
        check_init_tuple(tup, VariantWarning.expected_tuple_els, self.__class__.__name__)

        self.id = tup[0]
        self.message = tup[1]
        self.variant_id = tup[2]

    def __str__(self):
        return "{} - ID: {}, Message: {}, Variant ID: {}".format(self.__class__.__name__, self.id,
                                                                 self.message, self.variant_id)

    @staticmethod
    def get_all(conn) -> ['VariantWarning']:
        return get_all_db_objects(conn, VariantWarning, VariantWarning.table_name)

    @staticmethod
    def get_by_id(conn, warning_message_id) -> 'VariantWarning':
        return get_db_object_by_primary_id(conn, VariantWarning, VariantWarning.table_name,
                                           warning_message_id)

    @staticmethod
    def get_by_variant_id(conn, variant_id) -> ['VariantWarning']:
        return get_db_objects_by_foreign_id(conn, VariantWarning, VariantWarning.table_name,
                                            variant_id, VariantWarning.foreign_id_column)

    @staticmethod
    def get_by_variant_id_count(conn, variant_id) -> int:
        return get_foreign_id_count(conn, VariantWarning.table_name, variant_id,
                                    VariantWarning.foreign_id_column)


class VariantStdErr(object):
    table_name = "variant_stderr"
    foreign_id_column = "variant_id"
    expected_tuple_els = 3

    def __init__(self, tup):
        check_init_tuple(tup, VariantStdErr.expected_tuple_els, self.__class__.__name__)

        self.id = tup[0]
        self.message = tup[1]
        self.variant_id = tup[2]

    def __str__(self):
        return "{} - ID: {}, Message: {}, Variant ID: {}".format(self.__class__.__name__, self.id,
                                                                 self.message, self.variant_id)

    @staticmethod
    def get_all(conn) -> ['VariantStdErr']:
        return get_all_db_objects(conn, VariantStdErr, VariantStdErr.table_name)

    @staticmethod
    def get_by_id(conn, stderr_message_id) -> 'VariantStdErr':
        return get_db_object_by_primary_id(conn, VariantStdErr, VariantStdErr.table_name,
                                           stderr_message_id)

    @staticmethod
    def get_by_variant_id(conn, variant_id) -> ['VariantStdErr']:
        return get_db_objects_by_foreign_id(conn, VariantStdErr, VariantStdErr.table_name,
                                            variant_id, VariantStdErr.foreign_id_column)

    @staticmethod
    def get_by_variant_id_count(conn, variant_id) -> int:
        return get_foreign_id_count(conn, VariantStdErr.table_name, variant_id,
                                    VariantStdErr.foreign_id_column)


class UserSetting(object):
    table_name = "user_settings"
    foreign_id_column = "variant_id"
    expected_tuple_els = 4

    def __init__(self, tup):
        check_init_tuple(tup, UserSetting.expected_tuple_els, self.__class__.__name__)

        self.id = tup[0]
        self.name = tup[1]
        self.value = tup[2]
        self.variant_id = tup[3]

    def __str__(self):
        return "{} - ID: {}, Name: {}, Value: {}, Variant ID: {}".format(self.__class__.__name__,
                                                                         self.id, self.name, self.value,
                                                                         self.variant_id)

    @staticmethod
    def get_all(conn) -> ['UserSetting']:
        return get_all_db_objects(conn, UserSetting, UserSetting.table_name)

    @staticmethod
    def get_by_id(conn, user_setting_id) -> 'UserSetting':
        return get_db_object_by_primary_id(conn, UserSetting, UserSetting.table_name,
                                           user_setting_id)

    @staticmethod
    def get_by_variant_id(conn, variant_id) -> ['UserSetting']:
        return get_db_objects_by_foreign_id(conn, UserSetting, UserSetting.table_name,
                                            variant_id, UserSetting.foreign_id_column)


class Subtest(object):
    table_name = "subtests"
    foreign_id_column = "variant_id"
    expected_tuple_els = 3

    def __init__(self, tup):
        check_init_tuple(tup, Subtest.expected_tuple_els, self.__class__.__name__)

        self.id = tup[0]
        self.subtest_index = tup[1]
        self.variant_id = tup[2]

    def __str__(self):
        return "{} - ID: {}, Index: {}, Variant ID: {}".format(self.__class__.__name__, self.id,
                                                               self.subtest_index, self.variant_id)

    @staticmethod
    def get_all(conn) -> ['Subtest']:
        return get_all_db_objects(conn, Subtest, Subtest.table_name)

    @staticmethod
    def get_by_id(conn, subtest_id) -> 'Subtest':
        return get_db_object_by_primary_id(conn, Subtest, Subtest.table_name, subtest_id)

    @staticmethod
    def get_by_variant_id(conn, variant_id) -> ['Subtest']:
        return get_db_objects_by_foreign_id(conn, Subtest, Subtest.table_name,
                                            variant_id, Subtest.foreign_id_column)

    @staticmethod
    def get_by_variant_id_count(conn, variant_id) -> int:
        return get_foreign_id_count(conn, Subtest.table_name, variant_id,
                                    Subtest.foreign_id_column)


class Statistic(object):
    table_name = "statistics"
    foreign_id_column = "subtest_id"
    expected_tuple_els = 5

    def __init__(self, tup):
        check_init_tuple(tup, Statistic.expected_tuple_els, self.__class__.__name__)

        self.id = tup[0]
        self.name = tup[1]
        self.value = tup[2]
        self.result = tup[3]
        self.subtest_id = tup[4]

    def __str__(self):
        return "{} - ID: {}, Name: {}, Value: {}, Subtest ID: {}".format(self.__class__.__name__,
                                                                         self.id, self.name, self.value,
                                                                         self.subtest_id)

    @staticmethod
    def get_all(conn) -> ['Statistic']:
        return get_all_db_objects(conn, Statistic, Statistic.table_name)

    @staticmethod
    def get_by_id(conn, statistic_id) -> 'Statistic':
        return get_db_object_by_primary_id(conn, Statistic, Statistic.table_name, statistic_id)

    @staticmethod
    def get_by_subtest_id(conn, subtest_id) -> ['Statistic']:
        return get_db_objects_by_foreign_id(conn, Statistic, Statistic.table_name,
                                            subtest_id, Statistic.foreign_id_column)

    @staticmethod
    def get_by_subtest_id_count(conn, subtest_id) -> int:
        return get_foreign_id_count(conn, Statistic.table_name, subtest_id,
                                    Statistic.foreign_id_column)


class TestParameter(object):
    table_name = "test_parameters"
    foreign_id_column = "subtest_id"
    expected_tuple_els = 4

    def __init__(self, tup):
        check_init_tuple(tup, TestParameter.expected_tuple_els, self.__class__.__name__)

        self.id = tup[0]
        self.name = tup[1]
        self.value = tup[2]
        self.subtest_id = tup[3]

    def __str__(self):
        return "{} - ID: {}, Name: {}, Value: {}, Subtest ID: {}".format(self.__class__.__name__,
                                                                         self.id, self.name, self.value,
                                                                         self.subtest_id)

    @staticmethod
    def get_all(conn) -> ['TestParameter']:
        return get_all_db_objects(conn, TestParameter, TestParameter.table_name)

    @staticmethod
    def get_by_id(conn, test_parameter_id) -> 'TestParameter':
        return get_db_object_by_primary_id(conn, TestParameter, TestParameter.table_name,
                                           test_parameter_id)

    @staticmethod
    def get_by_subtest_id(conn, subtest_id) -> ['TestParameter']:
        return get_db_objects_by_foreign_id(conn, TestParameter, TestParameter.table_name,
                                            subtest_id, TestParameter.foreign_id_column)


class PValue(object):
    table_name = "p_values"
    foreign_id_column = "subtest_id"
    expected_tuple_els = 3

    def __init__(self, tup):
        check_init_tuple(tup, PValue.expected_tuple_els, self.__class__.__name__)

        self.id = tup[0]
        self.value = tup[1]
        self.subtest_id = tup[2]

    def __str__(self):
        return "{} - ID: {}, Value: {}, Subtest ID: {}".format(self.__class__.__name__,
                                                               self.id, self.value, self.subtest_id)

    @staticmethod
    def get_all(conn) -> ['PValue']:
        return get_all_db_objects(conn, PValue, PValue.table_name)

    @staticmethod
    def get_by_id(conn, p_value_id) -> 'PValue':
        return get_db_object_by_primary_id(conn, PValue, PValue.table_name, p_value_id)

    @staticmethod
    def get_by_subtest_id(conn, subtest_id) -> ['PValue']:
        return get_db_objects_by_foreign_id(conn, PValue, PValue.table_name,
                                            subtest_id, PValue.foreign_id_column)

    @staticmethod
    def get_by_subtest_id_count(conn, subtest_id) -> int:
        return get_foreign_id_count(conn, PValue.table_name,
                                    subtest_id, PValue.foreign_id_column)


'''
Helper utility methods here.
Only supposed to be used by the defined models not outside!!!
'''


def check_init_tuple(tup, expected_tuple_els, obj_name):
    if len(tup) != expected_tuple_els:
        raise ValueError("tuple for initializing {} must have {} fields but has {}"
                         .format(obj_name, expected_tuple_els, len(tup)))


def map_db_rows_to_objects(rows, db_obj):
    rval = []
    for row in rows:
        rval.append(db_obj(row))
        
    return rval


def get_all_db_objects(conn, db_obj, table_name):
    with conn.cursor() as c:
        c.execute("SELECT * FROM {}".format(table_name))
        return map_db_rows_to_objects(c.fetchall(), db_obj)


def get_db_object_by_primary_id(conn, db_obj, table_name, primary_id, primary_id_column="id"):
    with conn.cursor() as c:
        c.execute("SELECT * FROM {} WHERE {}=%s".format(table_name, primary_id_column), [primary_id])
        if c.rowcount > 1:
            raise LookupError("multiple rows with id={} in table {}"
                              .format(primary_id, table_name))
        if c.rowcount == 0:
            return None
        return map_db_rows_to_objects(c.fetchall(), db_obj)[0]


def get_db_objects_by_foreign_id(conn, db_obj, table_name, foreign_id, foreign_id_column):
    with conn.cursor() as c:
        c.execute("SELECT * FROM {} WHERE {}=%s".format(table_name, foreign_id_column), [foreign_id])
        return map_db_rows_to_objects(c.fetchall(), db_obj)


def get_all_count(conn, table_name) -> int:
    with conn.cursor() as c:
        c.execute("SELECT COUNT(1) FROM {}".format(table_name))
        return c.fetchone()[0]


def get_foreign_id_count(conn, table_name, foreign_id, foreign_id_column) -> int:
    with conn.cursor() as c:
        c.execute("SELECT COUNT(1) FROM {} WHERE {}=%s"
                  .format(table_name, foreign_id_column),
                  (foreign_id, ))
        return c.fetchone()[0]
