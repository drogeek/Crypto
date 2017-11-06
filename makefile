ORIGIN_FOLDER=original_images
TARGET_FOLDER=generated_images

IMG_TO_USE=balloons.ascii.pgm
hamming:
	echo "we show the original image"
	xdg-open ${ORIGIN_FOLDER}/${IMG_TO_USE}
	python3 genCrypt.py ${ORIGIN_FOLDER}/${IMG_TO_USE} ${TARGET_FOLDER}
	python3 genError.py ${TARGET_FOLDER}/enc_${IMG_TO_USE} ${TARGET_FOLDER}
	python3 genCorr.py ${TARGET_FOLDER}/e_enc_${IMG_TO_USE} ${TARGET_FOLDER}
	echo "and now the corrected image after having added noise to it"
	xdg-open ${TARGET_FOLDER}/cor_e_enc_${IMG_TO_USE}

clean:
	rm ${TARGET_FOLDER}/*

des:
	python3 des.py

reverse_des:
	python3 reverse_des.py
