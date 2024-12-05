# mySegmentation.py
# version="0.2.240829"


import numpy as np


""" 이미지 내에서 현재 픽셀의 상하좌우대각으로 연결된 점들을 찾는다.
"""
class Segmentation:
    def __init__(self, image):
        self.image = image

    def label_connected_pixels(self) -> tuple[np.ndarray, int]:
        image = self.image
        ''' label_connected_pixels'''
        labeled_image = np.zeros(image.shape)  # 레이블된 이미지를 저장할 배열 초기화
        current_label = 1  # 현재 레이블 값

        def get_neighbors(row, col):
            # 현재 픽셀의 상하좌우 이웃 픽셀 좌표 반환
            neighbors = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
            valid_neighbors = [(r, c) for r, c in neighbors if 0 <= r < image.shape[0] and 0 <= c < image.shape[1]]
            return valid_neighbors

        def dfs(row, col):
            # 깊이 우선 탐색을 통해 연결된 픽셀을 찾고 레이블을 할당함
            labeled_image[row, col] = current_label  # 현재 픽셀에 레이블 할당

            # 현재 픽셀의 이웃 픽셀 순회
            for neighbor_row, neighbor_col in get_neighbors(row, col):
                # 이웃 픽셀이 연결되어 있고 아직 레이블이 할당되지 않은 경우
                if image[neighbor_row, neighbor_col] and not labeled_image[neighbor_row, neighbor_col]:
                    dfs(neighbor_row, neighbor_col)  # 재귀적으로 깊이 우선 탐색 진행

        # 이미지 순회하며 라벨링
        for r in range(image.shape[0]):
            for c in range(image.shape[1]):
                # 현재 픽셀이 1인 경우에만 라벨링 진행
                if image[r, c] and not labeled_image[r, c]:
                    dfs(r, c)  # 연결된 픽셀 그룹을 찾기 위해 깊이 우선 탐색 수행
                    current_label += 1  # 새로운 그룹에 대해 새로운 레이블 값 할당

        number_of_features = np.max(labeled_image)
        return labeled_image, int(number_of_features)

    def areas(self):
        labeled_image, number_of_features = self.label_connected_pixels()
        areas = np.array([np.sum(labeled_image == i) for i in range(1, number_of_features+1)])
        return areas



class SegmentationWithDiagonal:
    """ 상하좌우대각으로 연속된 점들을 분류한다
    """
    def __init__(self, image):
        self.image = image

    def label_connected_pixels(self) -> tuple[np.ndarray, int]:
        """ 상하좌우대각으로 연결된 점들 집합에 레이블을 부여한다.
        """
        image = self.image
        labeled_image = np.zeros(image.shape)  # 레이블된 이미지를 저장할 배열 초기화
        current_label = 1  # 현재 레이블 값

        def get_neighbors(row, col):
            """ 현재 픽셀의 상하좌우대각 이웃 픽셀 좌표 반환
            """
            neighbors = [(row-1, col), (row+1, col), (row, col-1), (row, col+1),
                         (row-1, col-1), (row-1, col+1), (row+1, col+1), (row+1, col-1)]
            valid_neighbors = [(r, c) for r, c in neighbors if 0 <= r < image.shape[0] and 0 <= c < image.shape[1]]
            return valid_neighbors

        # 이미지 순회하며 라벨링
        for r in range(image.shape[0]):
            for c in range(image.shape[1]):
                # 현재 픽셀이 1인 경우에만 라벨링 진행
                if image[r, c] and not labeled_image[r, c]:
                    stack = [(r, c)]  # 스택에 현재 픽셀 좌표 추가
                    labeled_image[r, c] = current_label  # 현재 픽셀에 레이블 할당

                    # 스택이 빌 때까지 반복
                    while stack:
                        row, col = stack.pop()  # 스택에서 픽셀 좌표를 가져옴

                        # 현재 픽셀의 이웃 픽셀 순회
                        for neighbor_row, neighbor_col in get_neighbors(row, col):
                            # 이웃 픽셀이 연결되어 있고 아직 레이블이 할당되지 않은 경우
                            if image[neighbor_row, neighbor_col] and not labeled_image[neighbor_row, neighbor_col]:
                                labeled_image[neighbor_row, neighbor_col] = current_label  # 레이블 할당
                                stack.append((neighbor_row, neighbor_col))  # 스택에 이웃 픽셀 좌표 추가

                    current_label += 1  # 새로운 그룹에 대해 새로운 레이블 값 할당

        number_of_features = np.max(labeled_image)
        return labeled_image, int(number_of_features)

    def areas(self) -> np.ndarray:
        """ 연결점 레이블들의 픽셀수 합을 반환한다.
        """
        labeled_image, number_of_features = self.label_connected_pixels()
        areas = np.array([np.sum(labeled_image == i) for i in range(1, number_of_features+1)])
        return areas



class SegmentationWithDiagonal_recursion:
    """ 상하좌우대각으로 연속된 점들을 분류한다
        >> 재귀함수 제한깊이 제한 발생함 (최대 1000회까지 허용됨)
    """
    def __init__(self, image):
        self.image = image

    def label_connected_pixels(self) -> tuple[np.ndarray, int]:
        """ 상하좌우대각으로 연결된 점들 집합에 레이블을 부여한다.
        """
        image = self.image
        labeled_image = np.zeros(image.shape)  # 레이블된 이미지를 저장할 배열 초기화
        current_label = 1  # 현재 레이블 값

        def get_neighbors(row, col):
            """ 현재 픽셀의 상하좌우대각 이웃 픽셀 좌표 반환
            """
            neighbors = [(row-1, col), (row+1, col), (row, col-1), (row, col+1),
                         (row-1, col-1), (row-1, col+1), (row+1, col+1), (row+1, col-1)]
            valid_neighbors = [(r, c) for r, c in neighbors if 0 <= r < image.shape[0] and 0 <= c < image.shape[1]]
            return valid_neighbors

        def dfs(row, col):
            """ 깊이 우선 탐색을 통해 연결된 픽셀을 찾고 레이블을 할당함
            """
            labeled_image[row, col] = current_label  # 현재 픽셀에 레이블 할당

            # 현재 픽셀의 이웃 픽셀 순회
            for neighbor_row, neighbor_col in get_neighbors(row, col):
                # 이웃 픽셀이 연결되어 있고 아직 레이블이 할당되지 않은 경우
                if image[neighbor_row, neighbor_col] and not labeled_image[neighbor_row, neighbor_col]:
                    dfs(neighbor_row, neighbor_col)  # 재귀적으로 깊이 우선 탐색 진행

        # 이미지 순회하며 라벨링
        for r in range(image.shape[0]):
            for c in range(image.shape[1]):
                # 현재 픽셀이 1인 경우에만 라벨링 진행
                if image[r, c] and not labeled_image[r, c]:
                    dfs(r, c)  # 연결된 픽셀 그룹을 찾기 위해 깊이 우선 탐색 수행
                    current_label += 1  # 새로운 그룹에 대해 새로운 레이블 값 할당

        number_of_features = np.max(labeled_image)
        return labeled_image, int(number_of_features)

    def areas(self) -> np.ndarray:
        """ 연결점 레이블들의 픽셀수 합을 반환한다.
        """
        labeled_image, number_of_features = self.label_connected_pixels()
        areas = np.array([np.sum(labeled_image == i) for i in range(1, number_of_features+1)])
        return areas



