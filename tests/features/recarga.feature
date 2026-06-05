@recarga
Feature: Modulo de recargas celular - RecargaYa S.A.S.
  Como operador del sistema RecargaYa
  Quiero calcular el valor final de recargas de celular
  Para aplicar correctamente las bonificaciones de datos segun las reglas de negocio.

  # -------------------------------------------------------
  # Escenarios de validacion de monto
  # -------------------------------------------------------

  @smoke @critical
  Scenario: Recarga con monto fuera de rango inferior es rechazada
    Given un usuario estandar
    When intento realizar una recarga de 500 pesos
    Then la recarga es rechazada con un error de rango

  @smoke @critical
  Scenario: Recarga con monto fuera de rango superior es rechazada
    Given un usuario estandar
    When intento realizar una recarga de 60000 pesos
    Then la recarga es rechazada con un error de rango

  # -------------------------------------------------------
  # Escenarios de calculo de bonus
  # -------------------------------------------------------

  @smoke
  Scenario: Recarga valida sin bonus de datos
    Given un usuario estandar
    When realizo una recarga de 5000 pesos
    Then la recarga es aprobada
    And el porcentaje de bonus es 0.0
    And los datos de bonus son 0.0

  @critical
  Scenario: Recarga de 10000 pesos genera 10 por ciento de bonus
    Given un usuario estandar
    When realizo una recarga de 10000 pesos
    Then la recarga es aprobada
    And el porcentaje de bonus es 10.0
    And los datos de bonus son 1000.0

  @critical
  Scenario: Recarga de 30000 pesos genera 25 por ciento de bonus
    Given un usuario estandar
    When realizo una recarga de 30000 pesos
    Then la recarga es aprobada
    And el porcentaje de bonus es 25.0
    And los datos de bonus son 7500.0

  # -------------------------------------------------------
  # Scenario Outline: diferentes montos y tipos de usuario
  # -------------------------------------------------------

  @critical @regression
  Scenario Outline: Calculo de bonus segun monto y tipo de usuario
    Given un usuario <tipo_usuario>
    When realizo una recarga de <monto> pesos
    Then la recarga es aprobada
    And el porcentaje de bonus es <bonus_esperado>

    Examples:
      | tipo_usuario | monto | bonus_esperado |
      | estandar     | 1000  | 0.0            |
      | estandar     | 9999  | 0.0            |
      | estandar     | 10000 | 10.0           |
      | estandar     | 29999 | 10.0           |
      | estandar     | 30000 | 25.0           |
      | estandar     | 50000 | 25.0           |
      | premium      | 5000  | 0.0            |
      | premium      | 10000 | 15.0           |
      | premium      | 30000 | 30.0           |
