from rest_framework import serializers

from users.models import CustomUser as User
from .models import (Assignment, Question, Choice, GradedAssignment, Concept, 
    Note, SpecificExplanations, Topic, SubTopic)


class StringSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value


class QuestionSerializer(serializers.ModelSerializer):
    choices = StringSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'choices', 'question', 'order')


class AssignmentSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    teacher = StringSerializer(many=False)

    class Meta:
        model = Assignment
        fields = '__all__'

    def get_questions(self, obj):
        questions = QuestionSerializer(obj.questions.all(), many=True).data
        return questions

    def create(self, request):
        data = request.data

        assignment = Assignment()
        teacher = User.objects.get(username=data['teacher'])
        assignment.teacher = teacher
        assignment.title = data['title']
        assignment.save()

        order = 1
        for q in data['questions']:
            newQ = Question()
            newQ.question = q['title']
            newQ.order = order
            newQ.save()

            for c in q['choices']:
                newC = Choice()
                newC.title = c
                newC.save()
                newQ.choices.add(newC)

            newQ.answer = Choice.objects.get(title=q['answer'])
            newQ.assignment = assignment
            newQ.save()
            order += 1
        return assignment


class GradedAssignmentSerializer(serializers.ModelSerializer):
    student = StringSerializer(many=False)

    class Meta:
        model = GradedAssignment
        fields = '__all__'

    def create(self, request):
        data = request.data
        print(data)

        assignment = Assignment.objects.get(id=data['asntId'])
        student = User.objects.get(username=data['username'])

        graded_asnt = GradedAssignment()
        graded_asnt.assignment = assignment
        graded_asnt.student = student

        questions = [q for q in assignment.questions.all()]
        answers = [data['answers'][a] for a in data['answers']]

        answered_correct_count = 0
        for i in range(len(questions)):
            if questions[i].answer.title == answers[i]:
                answered_correct_count += 1
            i += 1

        grade = answered_correct_count / len(questions) * 100
        graded_asnt.grade = grade
        graded_asnt.save()
        return graded_asnt


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = "__all__"


class SubTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTopic
        fields = "__all__"


class ConceptSerializer(serializers.ModelSerializer):
    list_of_explanations = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Concept
        fields = "__all__"

    def get_list_of_explanations(self, obj):
        list_of_explanation = obj.list_of_explanations
        serializer = ListOfExplanationsSerializer(list_of_explanation, many=True)
        return serializer.data


class ListOfExplanationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificExplanations
        fields = "__all__"


class NoteSerializer(serializers.ModelSerializer):
    sub_topic = serializers.SerializerMethodField(read_only=True)
    notes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Note
        fields = "__all__"

    def get_sub_topic(self, obj):
        subtopic = obj.sub_topic
        serializer = SubTopicSerializer(subtopic, many=False)
        return serializer.data['name']

    def get_notes(self, obj):
        note = obj.notes
        serializer = ConceptSerializer(note, many=True)
        return serializer.data
