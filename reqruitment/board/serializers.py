from rest_framework import serializers
from .models import Board, BoardImage, User
from django.conf import settings
import boto3
import mimetypes

class BoardImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None

    class Meta:
        model = BoardImage
        fields = ['id', 'image_url']

class BoardListSerializer(serializers.ModelSerializer):
    content_preview = serializers.SerializerMethodField()

    def get_content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    class Meta:
        model = Board
        fields = ['id', 'title', 'created_at', 'content_preview']
        read_only_fields = ['created_at']

class BoardDetailSerializer(serializers.ModelSerializer):
    images = BoardImageSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'content', 'images', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class BoardSerializer(serializers.ModelSerializer):
    images = BoardImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False),
        write_only=True,
        required=False
    )
    images_to_keep = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    def create(self, validated_data):
        request = self.context.get('request')
        uploaded_images = request.FILES.getlist('uploaded_images') if request else []

        # admin_user 없으면 생성이 안 돼서 테스트할 때는 아래 코드 사용
        admin_user = User.objects.first()

        board = Board.objects.create(
            title=validated_data['title'],
            content=validated_data['content'],
            admin_user=admin_user
        )

        # s3 client 생성
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

        for image in uploaded_images:
            try:
                file_name = f'board_images/{board.id}_{image.name}'

                # # s3에 업로드
                # s3_client.upload_fileobj(
                #     image,
                #     settings.AWS_STORAGE_BUCKET_NAME,
                #     file_name,
                #     ExtraArgs={'ContentType': 'image/png'}
                # )

                s3_client.put_object(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                    Key=file_name,
                    Body=image,
                    ContentType='image/png'  # 강제로 Content-Type을 image/png로 설정
                )

                # BoardImage에 저장
                BoardImage.objects.create(
                    board=board,
                    image=file_name
                )

            except Exception as e:
                print(f"이미지 업로드 실패: {e}")

        return board

    def update(self, instance, validated_data):
        request = self.context.get('request')
        uploaded_images = request.FILES.getlist('uploaded_images', [])

        images_to_keep = request.POST.getlist('images_to_keep', [])

        # 이미지 외 수정 정보 저장
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()

        # s3 client 생성
        s3_client = boto3.client(
            's3', 
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

        # 이미지 일부 삭제
        for image in instance.images.all():
            if image.image.url not in images_to_keep:
                try:
                    s3_client.delete_object(
                        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                        Key=image.image.name
                    )
                    image.delete()
                except Exception as e:
                    print(f"S3 이미지 삭제 실패: {e}")

        for image in uploaded_images:
            try:
                file_name = f'board_images/{instance.id}_{image.name}'

                # s3에 업로드
                s3_client.upload_fileobj(
                    image,
                    settings.AWS_STORAGE_BUCKET_NAME,
                    file_name,
                    ExtraArgs={'ContentType': 'image/png'}
                )

                # BoardImage에 새 이미지 저장
                instance.images.create(image=file_name)
            except Exception as e:
                print(f"이미지 업로드 실패: {e}")
        
        return instance
    
    class Meta:
        model = Board
        fields = ['id', 'title', 'content', 'images', 'uploaded_images', 'images_to_keep', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']