import styled from "styled-components";

import {
    getImageUrl,
} from "../api/imageragApi";


const ImageRagResult = ({ data }) => {
    if (!data?.result) {
        return null;
    }

    const result = data.result;

    const confidencePercent =
        Math.round(result.confidence * 100);


    return (
        <Container>
            <Header>
                <div>
                    <Label>
                        분석 결과
                    </Label>

                    <FoodName>
                        {result.food_name}
                    </FoodName>
                </div>

                <Confidence>
                    {confidencePercent}%
                </Confidence>
            </Header>

            <InfoBox>
                <InfoTitle>
                    OpenAI 판단
                </InfoTitle>

                <Description>
                    {result.description}
                </Description>
            </InfoBox>

            <InfoBox>
                <InfoTitle>
                    매칭된 이미지 폴더
                </InfoTitle>

                <FolderName>
                    {result.matched_folder || "매칭 결과 없음"}
                </FolderName>
            </InfoBox>

            {result.reference_images?.length > 0 && (
                <ReferenceSection>
                    <ReferenceTitle>
                        관련 이미지
                    </ReferenceTitle>

                    <ImageGrid>
                        {result.reference_images.map(
                            (imagePath, index) => (
                                <ReferenceImage
                                    key={`${imagePath}-${index}`}
                                    src={getImageUrl(imagePath)}
                                    alt={`관련 이미지 ${index + 1}`}
                                />
                            )
                        )}
                    </ImageGrid>
                </ReferenceSection>
            )}
        </Container>
    );
};


export default ImageRagResult;


const Container = styled.div`
  width: 100%;

  display: flex;
  flex-direction: column;
  gap: 20px;
`;


const Header = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;

  padding-bottom: 20px;
  border-bottom: 1px solid #eaecf0;
`;


const Label = styled.div`
  font-size: 14px;
  color: #667085;

  margin-bottom: 6px;
`;


const FoodName = styled.h2`
  margin: 0;

  color: #101828;
  font-size: 32px;
`;


const Confidence = styled.div`
  min-width: 72px;

  padding: 10px 14px;

  border-radius: 20px;

  background: #ecfdf3;
  color: #027a48;

  font-size: 18px;
  font-weight: 700;

  text-align: center;
`;


const InfoBox = styled.div`
  padding: 18px;

  background: #f9fafb;

  border: 1px solid #eaecf0;
  border-radius: 12px;
`;


const InfoTitle = styled.div`
  margin-bottom: 8px;

  font-size: 13px;
  font-weight: 700;

  color: #667085;
`;


const Description = styled.div`
  line-height: 1.7;
  color: #344054;
`;


const FolderName = styled.div`
  color: #101828;
  font-size: 17px;
  font-weight: 700;
`;


const ReferenceSection = styled.div`
  display: flex;
  flex-direction: column;
  gap: 12px;
`;


const ReferenceTitle = styled.h3`
  margin: 0;

  font-size: 19px;
  color: #101828;
`;


const ImageGrid = styled.div`
  display: grid;

  grid-template-columns:
    repeat(
      auto-fill,
      minmax(140px, 1fr)
    );

  gap: 12px;
`;


const ReferenceImage = styled.img`
  width: 100%;
  height: 150px;

  object-fit: cover;

  border-radius: 10px;
  border: 1px solid #eaecf0;

  background: #f2f4f7;
`;