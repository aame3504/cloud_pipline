import styled from "styled-components";

import ImageUploader
    from "../components/ImageUploader";

import ImageRagResult
    from "../components/ImageRagResult";

import {
    useImageRagMutation,
} from "../query/useImageRagMutation";


const ImageRagPage = () => {
    const imageRagMutation =
        useImageRagMutation();


    const handleAnalyze = (imageFile) => {
        imageRagMutation.mutate(
            imageFile
        );
    };


    return (
        <PageContainer>
            <Header>
                <HeaderContent>
                    <Logo>
                        Image RAG
                    </Logo>

                    <SubTitle>
                        음식 이미지를 업로드하면
                        OpenAI가 이미지를 분석하고
                        관련 자료를 검색합니다.
                    </SubTitle>
                </HeaderContent>
            </Header>

            <Main>
                <Card>
                    <ImageUploader
                        onAnalyze={handleAnalyze}
                        isLoading={
                            imageRagMutation.isPending
                        }
                    />
                </Card>

                <Card>
                    {imageRagMutation.isPending && (
                        <LoadingBox>
                            <Spinner />

                            <LoadingTitle>
                                이미지를 분석하고 있습니다
                            </LoadingTitle>

                            <LoadingDescription>
                                OpenAI 이미지 분석 및
                                관련 이미지 검색 중입니다.
                            </LoadingDescription>
                        </LoadingBox>
                    )}

                    {imageRagMutation.isError && (
                        <ErrorBox>
                            <ErrorTitle>
                                분석 실패
                            </ErrorTitle>

                            <ErrorMessage>
                                {
                                    imageRagMutation
                                        .error
                                        .message
                                }
                            </ErrorMessage>
                        </ErrorBox>
                    )}

                    {imageRagMutation.isSuccess && (
                        <ImageRagResult
                            data={
                                imageRagMutation.data
                            }
                        />
                    )}

                    {!imageRagMutation.isPending &&
                        !imageRagMutation.isError &&
                        !imageRagMutation.isSuccess && (
                            <EmptyBox>
                                <EmptyIcon>
                                    IMG
                                </EmptyIcon>

                                <EmptyTitle>
                                    분석 결과가 여기에 표시됩니다
                                </EmptyTitle>

                                <EmptyDescription>
                                    왼쪽에서 음식 이미지를
                                    업로드하고 분석을 실행하세요.
                                </EmptyDescription>
                            </EmptyBox>
                        )}
                </Card>
            </Main>
        </PageContainer>
    );
};


export default ImageRagPage;


const PageContainer = styled.div`
  min-height: 100vh;
  background: #f2f4f7;
`;


const Header = styled.header`
  background: #101828;
  color: white;
`;


const HeaderContent = styled.div`
  width: min(1200px, calc(100% - 40px));
  margin: 0 auto;

  padding: 32px 0;
`;


const Logo = styled.h1`
  margin: 0 0 8px;

  font-size: 30px;
`;


const SubTitle = styled.div`
  color: #d0d5dd;
  line-height: 1.6;
`;


const Main = styled.main`
  width: min(1200px, calc(100% - 40px));

  margin: 0 auto;
  padding: 40px 0;

  display: grid;
  grid-template-columns: 1fr 1fr;

  gap: 24px;

  @media (max-width: 850px) {
    grid-template-columns: 1fr;
  }
`;


const Card = styled.section`
  min-height: 540px;

  padding: 28px;

  background: white;

  border: 1px solid #eaecf0;
  border-radius: 16px;

  box-shadow:
    0 2px 8px
    rgba(16, 24, 40, 0.05);
`;


const LoadingBox = styled.div`
  height: 100%;

  display: flex;
  flex-direction: column;

  align-items: center;
  justify-content: center;

  text-align: center;
`;


const Spinner = styled.div`
  width: 42px;
  height: 42px;

  margin-bottom: 20px;

  border: 4px solid #eaecf0;
  border-top-color: #101828;
  border-radius: 50%;

  animation: spin 0.8s linear infinite;

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
`;


const LoadingTitle = styled.h3`
  margin: 0 0 8px;
  color: #101828;
`;


const LoadingDescription = styled.p`
  margin: 0;
  color: #667085;
  line-height: 1.6;
`;


const ErrorBox = styled.div`
  padding: 20px;

  border: 1px solid #fda29b;
  border-radius: 12px;

  background: #fef3f2;
`;


const ErrorTitle = styled.h3`
  margin: 0 0 8px;
  color: #b42318;
`;


const ErrorMessage = styled.div`
  color: #b42318;
  line-height: 1.6;
`;


const EmptyBox = styled.div`
  height: 100%;

  display: flex;
  flex-direction: column;

  align-items: center;
  justify-content: center;

  text-align: center;
`;


const EmptyIcon = styled.div`
  width: 72px;
  height: 72px;

  margin-bottom: 18px;

  display: flex;
  align-items: center;
  justify-content: center;

  background: #f2f4f7;

  border-radius: 50%;

  color: #667085;
  font-size: 14px;
  font-weight: 700;
`;


const EmptyTitle = styled.h3`
  margin: 0 0 8px;

  color: #101828;
`;


const EmptyDescription = styled.p`
  margin: 0;

  color: #667085;
  line-height: 1.6;
`;