from graphene import ObjectType, Float, String, Int, Field, DateTime, List, __version__, Schema


class TestGraphene:
    package = "graphene"
    version = __version__

    def __init__(self, allow_extra):
        class Location(ObjectType):
            latitude = Float()
            longitude = Float()

        class Skill(ObjectType):
            subject = String()
            subject_id = Int()
            category = String()
            qual_level = String()
            qual_level_id = Int()
            qual_level_ranking = Float()

        class Model(ObjectType):
            id = Int()
            client_name = String()
            sort_index = Float()
            client_phone = String()

            location = Field(Location)

            contractor = Int()
            upstream_http_referrer = String()
            grecaptcha_response = String()
            last_updated = DateTime()
            skills = List(Skill)

        class Query(ObjectType):
            model = Field(Model)

            @staticmethod
            def resolve_model(root, _context):
                return Model(**root)

        self.allow_extra = allow_extra  # unused
        self.schema = Schema(Query)

    def validate(self, data):
        result, errors = self.schema.execute(
            source="""{ 
                model { 
                    id, 
                    clientName, 
                    sortIndex, 
                    clientPhone, 
                    location { 
                        latitude, 
                        longitude 
                    },
                    contractor,
                    upstreamHttpReferrer, 
                    grecaptchaResponse,
                    # lastUpdated,
                    skills {
                        subject,
                        subjectId,
                        category,
                        qualLevel,
                        qualLevelId,
                        qualLevelRanking
                    }
                } 
            }""",
            root_value=data,
        )

        if errors:
            return False, str(errors)

        return True, result
