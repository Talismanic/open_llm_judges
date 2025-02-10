from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import JudgeRequestSerializer
from .services.llm_judge import LLMJudgeSystem

class JudgeAPIView(APIView):
    """API Endpoint for running LLM Judge System"""

    def post(self, request):
        serializer = JudgeRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # Initialize LLM Judge System
            try:
                llm_system = LLMJudgeSystem(
                    archetype=data["archetype"],
                    num_agents=data["num_agents"],
                    task_meta=data["task_meta"],  # Now passed as a string
                    task=data["task"],
                    worker_agent_models=data["worker_agent_models"],  # Pass array of worker agents
                )
                result = llm_system.run()
                return Response(result, status=status.HTTP_200_OK)

            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ArchetypeListAPIView(APIView):
    """
    API View to return a list of available archetypes.
    """

    def get(self, request, *args, **kwargs):
        """
        Handle GET request and return predefined archetypes.
        """
        archetypes = [
            {"id": 1, "name": "single worker single judge"},
            {"id": 2, "name": "multiple worker single judge"},
            {"id": 3, "name": "majority consensus"},
        ]
        return Response({"archetypes": archetypes})
