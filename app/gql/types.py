from graphene import ObjectType, String, Int


class EmployerObject(ObjectType):
    id = Int()
    name = String()
    contact_email = String()
    industry = String()


class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()


class UserObject(ObjectType):
    id = Int()
    username = String()
    email = String()
    role = String()


class JobApplicationObject(ObjectType):
    id = Int()
    user_id = Int()
    job_id = Int()
