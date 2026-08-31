import { useEffect, useState } from "react";
import styled from "styled-components";


const ImageUploader = ({
                           onAnalyze,
                           isLoading,
                       }) => {
    const [selectedFile, setSelectedFile] =
        useState(null);

    const [previewUrl, setPreviewUrl] =
        useState(null);


    useEffect(() => {
        if (!selectedFile) {
            setPreviewUrl(null);
            return;
        }

        const url = URL.createObjectURL(
            selectedFile
        );

        setPreviewUrl(url);

        return () => {
            URL.revokeObjectURL(url);
        };
    }, [selectedFile]);


    const handleFileChange = (event) => {
        const file =
            event.target.files?.[0];

        if (!file) {
            return;
        }

        if (!file.type.startsWith("image/")) {
            alert("이미지 파일만 선택할 수 있습니다.");
            return;
        }

        setSelectedFile(file);
    };


    const handleAnalyze = () => {
        if (!selectedFile) {
            alert("이미지를 선택해주세요.");
            return;
        }

        onAnalyze(selectedFile);
    };


    return (
        <Container>
            <Title>
                음식 이미지 업로드
            </Title>

            <UploadBox>
                {previewUrl ? (
                    <PreviewImage
                        src={previewUrl}
                        alt="업로드 이미지"
                    />
                ) : (
                    <Placeholder>
                        이미지를 선택해주세요
                    </Placeholder>
                )}
            </UploadBox>

            <FileInputLabel>
                이미지 선택

                <FileInput
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                />
            </FileInputLabel>

            {selectedFile && (
                <FileName>
                    {selectedFile.name}
                </FileName>
            )}

            <AnalyzeButton
                onClick={handleAnalyze}
                disabled={
                    !selectedFile ||
                    isLoading
                }
            >
                {isLoading
                    ? "분석 중..."
                    : "Image RAG 분석"}
            </AnalyzeButton>
        </Container>
    );
};


export default ImageUploader;


const Container = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
`;


const Title = styled.h2`
  margin: 0;
  font-size: 24px;
  color: #202124;
`;


const UploadBox = styled.div`
  width: 100%;
  height: 360px;

  border: 2px dashed #d0d5dd;
  border-radius: 16px;

  background: #f8fafc;

  display: flex;
  align-items: center;
  justify-content: center;

  overflow: hidden;
`;


const PreviewImage = styled.img`
  width: 100%;
  height: 100%;
  object-fit: contain;
`;


const Placeholder = styled.div`
  color: #98a2b3;
  font-size: 16px;
`;


const FileInputLabel = styled.label`
  display: flex;
  align-items: center;
  justify-content: center;

  height: 48px;

  border: 1px solid #d0d5dd;
  border-radius: 10px;

  background: white;

  font-weight: 600;
  cursor: pointer;

  &:hover {
    background: #f9fafb;
  }
`;


const FileInput = styled.input`
  display: none;
`;


const FileName = styled.div`
  font-size: 14px;
  color: #667085;

  word-break: break-all;
`;


const AnalyzeButton = styled.button`
  width: 100%;
  height: 52px;

  border: none;
  border-radius: 10px;

  background: #101828;
  color: white;

  font-size: 16px;
  font-weight: 700;

  cursor: pointer;

  &:disabled {
    background: #d0d5dd;
    cursor: not-allowed;
  }

  &:not(:disabled):hover {
    background: #344054;
  }
`;